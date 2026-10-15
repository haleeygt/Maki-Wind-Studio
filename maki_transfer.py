"""LoggerNet ingestion: same reader and atomic project store as the application."""
import datetime, hashlib, json, os, re, threading, uuid
from pathlib import Path
import numpy as np
import pandas as pd
LOCK = threading.RLock()
ROOT = Path(__file__).resolve().parent / '.maki_runtime' / 'cloud_projects'
RUZGAR_KOLONLARI = [
    "WS1_Avg",
    "WS2_Avg",
    "WS3_Avg",
    "WS4_Avg"
]
def loggernet_oku(dosya_bytes):
    """LoggerNet TOA5 veya standart CSV WindData dosyasını güvenli biçimde okur.

    Header satırı sabit kabul edilmez; ilk satırlarda TIMESTAMP aranır. Böylece
    farklı LoggerNet export şablonları ve BOM içeren dosyalar aynı okuyucudan geçer.
    """
    from io import StringIO

    if isinstance(dosya_bytes, bytes):
        metin = dosya_bytes.decode("utf-8-sig", errors="replace")
    else:
        metin = str(dosya_bytes)

    satirlar = metin.splitlines()
    header_idx = None
    for i, satir in enumerate(satirlar[:12]):
        if re.search(r'(^|[,;\t\"])(timestamp|date\s*time|datetime)([,;\t\"]|$)', satir, re.I):
            header_idx = i
            break
    if header_idx is None:
        # Eski standart TOA5 yapısına geri dönüş.
        header_idx = 1 if len(satirlar) > 1 else 0

    # LoggerNet TOA5 esas olarak virgüllüdür. Standart CSV/TXT için ayırıcıyı
    # header satırından seç; pandas python engine quoted alanları korur.
    header_line = satirlar[header_idx] if header_idx < len(satirlar) else ""
    if ';' in header_line and header_line.count(';') > header_line.count(','):
        sep = ';'
    elif '\t' in header_line and header_line.count('\t') > header_line.count(','):
        sep = '\t'
    else:
        sep = ','

    veri = pd.read_csv(StringIO(metin), header=header_idx, sep=sep, engine='python')
    veri.columns = [str(k).strip().strip('"').lstrip('\ufeff') for k in veri.columns]

    # TIMESTAMP adının büyük/küçük harf veya DateTime varyasyonlarını normalize et.
    ts_kolonu = None
    for kolon in veri.columns:
        norm = re.sub(r'[^a-z0-9]+', '', str(kolon).lower())
        if norm in {'timestamp', 'datetime', 'dateandtime', 'date_time'}:
            ts_kolonu = kolon
            break
    if ts_kolonu is None:
        raise ValueError('TIMESTAMP/DateTime kolonu bulunamadı.')
    if ts_kolonu != 'TIMESTAMP':
        veri = veri.rename(columns={ts_kolonu: 'TIMESTAMP'})

    _logger_metadata = pd.Series(False, index=veri.index)
    _first_rows = veri.head(4)
    _logger_metadata.loc[_first_rows.index] = (_first_rows['TIMESTAMP'].astype(str).eq('TS')
        | _first_rows.isin(['Avg','Smp','WVc','Std']).any(axis=1))
    veri['TIMESTAMP'] = pd.to_datetime(veri['TIMESTAMP'], errors='coerce')
    for kolon in [k for k in veri.columns if k != 'TIMESTAMP']:
        veri[kolon] = pd.to_numeric(veri[kolon], errors='coerce')

    _invalid_timestamp_count = int((veri['TIMESTAMP'].isna() & ~_logger_metadata).sum())
    veri = veri.dropna(subset=['TIMESTAMP']).sort_values('TIMESTAMP').reset_index(drop=True)
    veri.attrs["discarded_invalid_times"] = _invalid_timestamp_count
    if veri.empty:
        raise ValueError('Dosyada geçerli zaman damgalı kayıt bulunamadı.')
    measured = [c for c in veri.columns if re.fullmatch(r"WS\d+_Avg", str(c), re.I)]
    if not measured:
        raise ValueError("WS1_Avg benzeri hız kanalı bulunamadı. Dosyanın hız sütunları eşleştirilmelidir.")
    veri.attrs["measured_speed_columns"] = measured
    for c in RUZGAR_KOLONLARI:
        if c not in veri.columns:
            veri[c] = np.nan  # Ölçüm olmayan kanal; gerçek veri üretilmez.
    return veri

class ProjectStore:
    def __init__(self, pid):
        if not re.fullmatch(r"[a-f0-9]{64}", pid):
            raise ValueError("Geçersiz proje")
        self.pid = pid
    def _bulut_proje_dizini(self):
        return ROOT / self.pid
    def _bulut_proje_kilidi(self):
        return LOCK
    def _bulut_manifest_oku(self):
        path = self._bulut_proje_dizini() / 'manifest.json'
        if not path.exists():
            return {'schema': 1, 'revision': None, 'files': [], 'settings': {}}
        manifest = json.loads(path.read_text(encoding='utf-8'))
        if manifest.get('schema') != 1 or not isinstance(manifest.get('files'), list):
            raise ValueError('Bulut proje kaydı okunamadı; son çalışma verisi korunuyor.')
        return manifest

    def _bulut_manifest_yaz(self, manifest):
        root = self._bulut_proje_dizini()
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        manifest['revision'] = uuid.uuid4().hex
        temp = root / ('.manifest-' + uuid.uuid4().hex + '.tmp')
        try:
            temp.write_text(json.dumps(manifest, ensure_ascii=False, default=str), encoding='utf-8')
            os.replace(temp, root / 'manifest.json')
        finally:
            temp.unlink(missing_ok=True)

    def _bulut_kayitlari(self, manifest):
        records = []
        for item in manifest['files']:
            digest = item.get('sha256', '')
            if not re.fullmatch(r'[a-f0-9]{64}', digest):
                raise ValueError('Bulut dosya imzası geçersiz; çalışma verisi değiştirilmedi.')
            path = self._bulut_proje_dizini() / (digest + '.dat')
            if not path.is_file() or path.stat().st_size != item['size']:
                raise ValueError('Bulut aktarımı eksik; çalışma verisi değiştirilmedi.')
            records.append({**item, 'source_path': str(path), 'source': 'browser_loggernet',
                            'type': 'text/plain'})
        return records

    def bulut_loggernet_yayinla(self, record):
        """Commit a verified whole-file snapshot atomically; preserve other masts and settings."""
        content = record.get('bytes')
        if content is None and record.get('source_path'):
            content = Path(record['source_path']).read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest != record.get('sha256') or len(content) != record['size']:
            raise ValueError('Buluta kaydetmeden önce dosya bütünlüğü kontrolü başarısız.')
        with self._bulut_proje_kilidi():
            manifest = self._bulut_manifest_oku()
            files = list(manifest['files'])
            if any(x['folder_id'] != record['folder_id'] for x in files):
                raise ValueError('Bu projeye başka bir klasör bağlı; farklı direk grupları karıştırılmaz.')
            names = [x['name'] for x in files]
            if record['name'] not in names and any(n.casefold() == record['name'].casefold() for n in names):
                raise ValueError('Aynı adlı dosyalar birleştirilemez.')
            metadata = {k: record[k] for k in ('name', 'sha256', 'size', 'folder_id', 'mtime_ms')}
            metadata['received_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
            if record['name'] in names:
                files[names.index(record['name'])] = metadata
            else:
                files.append(metadata)
            if sum(x['size'] for x in files) > 256 * 1024 * 1024:
                raise ValueError('Bu proje için 256 MB aktarım sınırı aşıldı; önceki veri korundu.')
            root = self._bulut_proje_dizini()
            root.mkdir(parents=True, exist_ok=True, mode=0o700)
            blob = root / (digest + '.dat')
            # Rewrite even an existing same-hash cache if its bytes were damaged.
            if not blob.exists() or hashlib.sha256(blob.read_bytes()).hexdigest() != digest:
                temp = root / ('.file-' + uuid.uuid4().hex + '.tmp')
                try:
                    temp.write_bytes(content)
                    os.replace(temp, blob)
                finally:
                    temp.unlink(missing_ok=True)
            manifest['files'] = files
            self._bulut_manifest_yaz(manifest)
            # Keep retired blobs briefly so another browser can finish an in-flight read.
            current = {x['sha256'] + '.dat' for x in files}
            retired = manifest.setdefault('retired', {})
            now = datetime.datetime.now(datetime.timezone.utc).timestamp()
            for previous in root.glob('*.dat'):
                if previous.name in current:
                    retired.pop(previous.name, None)
                else:
                    retired.setdefault(previous.name, now)
                    if now - retired[previous.name] > 600:
                        try:
                            previous.unlink()
                            retired.pop(previous.name, None)
                        except OSError:
                            pass
            if retired or 'retired' in manifest:
                # Atomic rewrite retains the already chosen revision and file ordering.
                temp = root / ('.manifest-' + uuid.uuid4().hex + '.tmp')
                try:
                    temp.write_text(json.dumps(manifest, ensure_ascii=False, default=str), encoding='utf-8')
                    os.replace(temp, root / 'manifest.json')
                finally:
                    temp.unlink(missing_ok=True)
            return self._bulut_kayitlari(manifest), manifest['revision']

