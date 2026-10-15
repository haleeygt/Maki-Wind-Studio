"""A viewer receives HTTP uploads with no folder picker or source Chrome tab."""
from pathlib import Path
import hashlib, json, os, re, sys, urllib.request, uuid
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from maki_transfer import ProjectStore
URL=os.environ.get('MAKI_TEST_URL','http://127.0.0.1:8511')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context()
 context.add_init_script("window.folderPickerCalls=0;window.showDirectoryPicker=async()=>{window.folderPickerCalls++;throw new Error('Not allowed in viewer')}")
 page=context.new_page();page.goto(URL,wait_until='networkidle')
 expect(page.get_by_text('Bu projeye henüz veri aktarılmadı.',exact=False)).to_be_visible(timeout=30000)
 pid=parse_qs(urlparse(page.url).query)['pid'][0]
 req=urllib.request.Request(URL+'/maki-sync/v1/status',headers={'Authorization':'Bearer '+pid})
 with urllib.request.urlopen(req) as res: assert json.load(res)['known']=={}
 print('PASS opening the app creates an upload-ready private project',flush=True)
 page.get_by_role('button',name='⇧ Veri Yükleme ve Direk Ayarları',exact=False).click()
 if not page.get_by_role('button',name='Windows LoggerNet yardımcısını indir').is_visible():page.get_by_text('LoggerNet otomatik bağlantı',exact=True).click()
 expect(page.get_by_role('button',name='Windows LoggerNet yardımcısını indir')).to_be_visible()
 with page.expect_download() as download:
  page.get_by_role('button',name='Windows LoggerNet yardımcısını indir').click()
 text=Path(download.value.path()).read_text()
 assert ('PROJECT_URL = ' + repr(URL.rstrip('/') + '/?pid=' + pid)) in text
 assert 'hpypuh736bbxr6pjr9jua4' not in text
 assert 'msid=' not in next(line for line in text.splitlines() if line.startswith('PROJECT_URL ='))
 print('PASS private helper download is paired only with the active project',flush=True)
 data=('TIMESTAMP,WS1_Avg,WS2_Avg\n'+''.join(f'2025-01-01 {i//6:02}:{i%6*10:02}:00,6.2,6.0\n' for i in range(144))).encode()
 digest=hashlib.sha256(data).hexdigest()
 metadata={'name':'OtherMast_WindData.dat','size':len(data),'sha256':digest,'mtime_ms':1,'folder_id':str(uuid.uuid4())}
 req=urllib.request.Request(URL+'/maki-sync/v1/file',data=data,headers={'Authorization':'Bearer '+pid,'X-Maki-Metadata':json.dumps(metadata)})
 with urllib.request.urlopen(req) as res:assert json.load(res)['ok']
 expect(page.get_by_text('Ortak projede 1 LoggerNet dosyası var.',exact=False)).to_be_visible(timeout=30000)
 frame=next(f for f in page.frames if 'maki_browser_loggernet_v1' in f.url)
 frame.wait_for_function("digest=>args.known?.['OtherMast_WindData.dat']===digest",arg=digest,timeout=30000)
 assert frame.evaluate('window.folderPickerCalls')==0
 assert page.locator('[data-testid="stException"]').count()==0
 print('PASS HTTPS-route upload appears in viewer automatically without Chrome source or folder permission',flush=True)
 page.screenshot(path='/tmp/maki_background21.png',full_page=True)
 browser.close()
