"""Authenticated streaming upload routes for Streamlit's public st.App API."""
import asyncio
import hashlib
import json
import re
import uuid
from starlette.responses import JSONResponse
from starlette.routing import Route
from maki_transfer import ProjectStore, LOCK, loggernet_oku

LIMIT = 64 * 1024 * 1024
_GATE = asyncio.Semaphore(1)

def reply(data, status=200):
    return JSONResponse(data, status_code=status, headers={'Cache-Control': 'no-store'})

def authenticate(request):
    auth = request.headers.get('authorization', '')
    if not re.fullmatch(r'Bearer [a-f0-9]{64}', auth):
        return None
    store = ProjectStore(auth[7:])
    # No project creation, enumeration, or fallback to another user's project.
    return store if (store._bulut_proje_dizini() / 'manifest.json').is_file() else None

async def status(request):
    store = authenticate(request)
    if store is None:
        return reply({'error': 'Proje bağlantısı geçersiz veya proje henüz hazır değil.'}, 401)
    with LOCK:
        manifest = store._bulut_manifest_oku()
        hashes = {}
        for item in manifest['files']:
            digest = item.get('sha256', '')
            if not re.fullmatch('[a-f0-9]{64}', digest):
                continue
            path = store._bulut_proje_dizini() / (digest + '.dat')
            if path.is_file() and path.stat().st_size == item['size']:
                with path.open('rb') as source:
                    actual = hashlib.file_digest(source, 'sha256').hexdigest()
                if actual == digest:
                    hashes[item['name']] = digest
    return reply({'protocol': 1, 'known': hashes,
                  'folder_id': manifest['files'][0]['folder_id'] if manifest['files'] else None})

async def upload(request):
    store = authenticate(request)
    if store is None:
        return reply({'error': 'Yetkisiz proje.'}, 401)
    try:
        metadata = json.loads(request.headers.get('x-maki-metadata', ''))
        name, size = metadata['name'], metadata['size']
        if not isinstance(name, str) or len(name) > 240 or any(c in name for c in '/\\\x00') or not name.lower().endswith('winddata.dat') or 'rawdata' in name.lower():
            raise ValueError('Geçersiz WindData dosyası.')
        if type(size) is not int or not 0 < size <= LIMIT:
            raise ValueError('Dosya boyutu sınırı aşıldı.')
        if not re.fullmatch('[a-f0-9]{64}', metadata['sha256']):
            raise ValueError('Geçersiz dosya imzası.')
        if str(uuid.UUID(metadata['folder_id'])) != metadata['folder_id']:
            raise ValueError('Geçersiz klasör kimliği.')
        mtime = metadata['mtime_ms']
        if type(mtime) not in (int, float) or not 0 <= mtime < 1e16:
            raise ValueError('Geçersiz tarih.')
    except (KeyError, TypeError, ValueError):
        return reply({'error': 'Aktarım bilgileri geçersiz.'}, 400)
    if _GATE.locked():
        return reply({'error': 'Sunucu meşgul; aktarım yeniden denenecek.'}, 429)
    async with _GATE:
        try:
            async with asyncio.timeout(180):
                content = bytearray()
                async for chunk in request.stream():
                    if len(content) + len(chunk) > size:
                        return reply({'error': 'Boyut uyuşmuyor.'}, 400)
                    content.extend(chunk)
            if len(content) != size or hashlib.sha256(content).hexdigest() != metadata['sha256'] or not content.endswith(b'\n'):
                return reply({'error': 'Eksik dosya veya imza uyuşmazlığı; önceki veri korundu.'}, 400)
            def validate_publish():
                data = bytes(content)
                parsed = loggernet_oku(data)
                if parsed.empty or parsed.attrs.get('discarded_invalid_times', 0):
                    raise ValueError('Bozuk zaman kaydı.')
                del parsed
                return store.bulut_loggernet_yayinla({**metadata, 'bytes': data})
            _, revision = await asyncio.to_thread(validate_publish)
            return reply({'ok': True, 'sha256': metadata['sha256'], 'revision': revision})
        except (ValueError, UnicodeError):
            return reply({'error': 'Ölçüm dosyası doğrulanamadı; önceki veri korundu.'}, 400)
        except TimeoutError:
            return reply({'error': 'Aktarım zaman aşımı; tekrar denenecek.'}, 408)
        except Exception:
            return reply({'error': 'Aktarım tamamlanamadı; önceki veri korundu.'}, 503)

upload_routes = [Route('/maki-sync/v1/status', status, methods=['GET']),
                 Route('/maki-sync/v1/file', upload, methods=['POST'])]
