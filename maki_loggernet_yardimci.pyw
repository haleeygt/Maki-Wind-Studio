"""Maki LoggerNet v11.11.22: read-only sender; Python standard library only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import uuid

PROJECT_URL = ''  # Set only in a private download, never in the public repository.
ROOT = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / 'MakiWindStudio'
CONFIG = ROOT / 'ayarlar.json'
AGENT = ROOT / 'maki_loggernet_yardimci.pyw'

def connection(url):
    parsed = urllib.parse.urlsplit(url.strip())
    pid = urllib.parse.parse_qs(parsed.query).get('pid', [''])[0]
    import re
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or not re.fullmatch('[a-f0-9]{64}', pid):
        raise ValueError('Uygulamadaki özel proje bağlantısını kullanın (https ve pid gerekli).')
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, '', '', '')), pid

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward a private bearer token to a redirected hostname.
        raise ValueError('Sunucu yönlendirmesi reddedildi.')

OPENER = urllib.request.build_opener(NoRedirect())

def request(config, path, data=None, metadata=None):
    base, token = connection(config['url'])
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
    if metadata:
        headers['X-Maki-Metadata'] = json.dumps(metadata, ensure_ascii=True)
        headers['Content-Type'] = 'application/octet-stream'
    req = urllib.request.Request(base + '/maki-sync/v1/' + path, data=data, headers=headers)
    with OPENER.open(req, timeout=180) as response:
        if response.headers.get_content_type() != 'application/json':
            raise ValueError('Sunucu aktarım bağlantısı henüz hazır değil.')
        return json.loads(response.read(32768))

def snapshot(path):
    first = path.stat()
    if not 0 < first.st_size <= 64 * 1024 * 1024:
        return None
    data = path.read_bytes()
    last = path.stat()
    if (first.st_size, first.st_mtime_ns) != (last.st_size, last.st_mtime_ns) or not data.endswith(b'\n'):
        return None
    return data, hashlib.sha256(data).hexdigest(), last.st_mtime_ns // 1000000

def scan(config):
    remote = request(config, 'status')
    if remote.get('protocol') != 1:
        raise ValueError('Uyumsuz sunucu sürümü.')
    folder_id = remote.get('folder_id') or config['folder_id']
    sent = 0
    for path in sorted(Path(config['folder']).iterdir()):
        if not path.is_file() or not path.name.lower().endswith('winddata.dat') or 'rawdata' in path.name.lower():
            continue
        item = snapshot(path)
        if item is None:
            continue
        data, digest, mtime = item
        if remote['known'].get(path.name) == digest:
            continue
        result = request(config, 'file', data, {'name': path.name, 'size': len(data),
            'sha256': digest, 'mtime_ms': mtime, 'folder_id': folder_id})
        if not result.get('ok') or result.get('sha256') != digest:
            raise ValueError('Sunucu dosyayı doğrulamadı.')
        sent += 1
    return sent

def autorun(enable):
    import winreg
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run') as key:
        if enable:
            interpreter = Path(sys.executable).with_name('pythonw.exe')
            winreg.SetValueEx(key, 'MakiWindStudioLoggerNet', 0, winreg.REG_SZ,
                subprocess.list2cmdline([str(interpreter), str(AGENT), '--watch']))
        else:
            try: winreg.DeleteValue(key, 'MakiWindStudioLoggerNet')
            except FileNotFoundError: pass

def watch():
    # OS mutex prevents duplicate startup processes without leaving stale lockfiles.
    import ctypes
    from ctypes import wintypes
    ctypes.windll.kernel32.CreateMutexW.restype = wintypes.HANDLE
    ctypes.windll.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, 'Local\\MakiWindStudioLoggerNet')
    if ctypes.windll.kernel32.GetLastError() == 183:
        return
    delay = 30
    try:
        while CONFIG.exists():
            try:
                config = json.loads(CONFIG.read_text(encoding='utf-8'))
                if not config.get('enabled'): return
                count = scan(config)
                message = 'Bağlı; dosyalar güncel.' if not count else f'{count} dosya aktarıldı.'
                delay = 30
            except Exception:
                message = 'Bağlantı bekleniyor; mevcut bulut verisi korunuyor.'
                delay = min(delay * 2, 300)
            temp = ROOT / 'durum.tmp'
            temp.write_text(json.dumps({'time': time.time(), 'message': message}, ensure_ascii=False), encoding='utf-8')
            os.replace(temp, ROOT / 'durum.json')
            time.sleep(delay)
    finally:
        ctypes.windll.kernel32.CloseHandle(mutex)

def settings():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    if sys.platform != 'win32':
        raise RuntimeError('Bu yardımcı Windows içindir.')
    existing = json.loads(CONFIG.read_text(encoding='utf-8')) if CONFIG.exists() else {}
    window = tk.Tk(); window.title('Maki LoggerNet bağlantısı · v11.11.22'); window.geometry('620x330')
    url = tk.StringVar(value=existing.get('url', PROJECT_URL))
    folder = tk.StringVar(value=existing.get('folder', r'C:\Campbellsci\veriler'))
    enabled = tk.BooleanVar(value=existing.get('enabled', True))
    tk.Label(window, text='Özel proje bağlantısı (uygulamada otomatik doldurulur)').pack(pady=(15, 4))
    tk.Entry(window, textvariable=url, width=85, show='•').pack()
    tk.Label(window, text='LoggerNet klasörü — yalnızca WindData.dat dosyaları okunur').pack(pady=(12, 4))
    tk.Entry(window, textvariable=folder, width=85).pack()
    def choose():
        selected = filedialog.askdirectory(initialdir=folder.get())
        if selected: folder.set(selected)
    tk.Button(window, text='Klasörü seç', command=choose).pack(pady=5)
    tk.Checkbutton(window, text='Windows oturumu açıldığında takip et', variable=enabled).pack()
    tk.Label(window, text='Chrome açık kalmaz. Bilgisayar ve internet açık olmalıdır.\nHam dosyalar değiştirilmez. Kapatmak için bu dosyayı yeniden açın.').pack(pady=8)
    def save():
        try:
            config = {'url': url.get().strip(), 'folder': folder.get(), 'enabled': enabled.get(),
                      'folder_id': existing.get('folder_id', str(uuid.uuid4()))}
            connection(config['url'])
            if enabled.get():
                if not Path(config['folder']).is_dir(): raise ValueError('LoggerNet klasörü bulunamadı.')
                request(config, 'status')  # Fail before changing Windows startup configuration.
            ROOT.mkdir(parents=True, exist_ok=True)
            # Restrict the bearer configuration to the current Windows user and SYSTEM.
            user = subprocess.check_output(['whoami', '/user', '/fo', 'csv', '/nh'], text=True).strip().split(',')[-1].strip('"')
            subprocess.run(['icacls', str(ROOT), '/inheritance:r', '/grant:r', f'*{user}:(OI)(CI)F', '*S-1-5-18:(OI)(CI)F'], check=True, capture_output=True, creationflags=0x08000000)
            if Path(__file__).resolve() != AGENT.resolve(): shutil.copyfile(__file__, AGENT)
            temp = ROOT / 'ayarlar.tmp'; temp.write_text(json.dumps(config), encoding='utf-8'); os.replace(temp, CONFIG)
            autorun(enabled.get())
            if enabled.get():
                pythonw = Path(sys.executable).with_name('pythonw.exe')
                subprocess.Popen([str(pythonw), str(AGENT), '--watch'], creationflags=0x08000000)
            messagebox.showinfo('Maki Wind Studio', 'Bağlantı kaydedildi. Chrome’u kapatabilirsiniz.' if enabled.get() else 'Otomatik takip kapatıldı (en geç 5 dakika içinde).')
            window.destroy()
        except Exception:
            messagebox.showerror('Bağlantı kurulamadı', 'Proje bağlantısını, klasörü ve interneti kontrol edin. Sunucuda v11.11.22 aktarım servisi etkin olmalıdır. Hiçbir ölçüm dosyası değiştirilmedi.')
    tk.Button(window, text='Kaydet ve bağlan', command=save).pack(pady=6)
    window.mainloop()

if __name__ == '__main__':
    watch() if '--watch' in sys.argv else settings()
