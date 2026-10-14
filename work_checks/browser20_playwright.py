"""Two isolated browser contexts share a capability URL, not local folder permissions."""
from pathlib import Path
import base64,hashlib,os
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('MAKI_TEST_URL','http://127.0.0.1:8509')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 chrome=browser.new_context(viewport={'width':1440,'height':1000})
 source=chrome.new_page();source.goto(URL,wait_until='networkidle')
 source.get_by_role('button',name='⇧ Veri Yükleme ve Direk Ayarları',exact=False).click()
 source_frame=source.frame_locator('iframe[title$="maki_browser_loggernet_v1"]')
 if not source_frame.get_by_role('button',name='Klasörü bağla / izni yenile').is_visible():
  source.get_by_text('LoggerNet otomatik bağlantı',exact=True).click()
 source_frame.get_by_role('button',name='Klasörü bağla / izni yenile').wait_for()
 frame=next(f for f in source.frames if 'maki_browser_loggernet_v1' in f.url)
 frame.evaluate('''async()=>{
 const root=await navigator.storage.getDirectory();
 window.testDir=await root.getDirectoryHandle('source-folder',{create:true});
 window.fixture=speed=>['TIMESTAMP,WS1_Avg,WS2_Avg,WS3_Avg,WS4_Avg,WD1_Avg,WD2_Avg',...Array.from({length:144},(_,i)=>`${new Date(Date.UTC(2025,0,1,0,i*10)).toISOString().replace('T',' ').slice(0,19)},${speed},5.8,5.5,5,200,210`)].join('\\n')+'\\n';
 window.put=async(name,text)=>{const h=await testDir.getFileHandle(name,{create:true});const w=await h.createWritable();await w.write(text);await w.close()};
 await put('Generic_WindData.dat',fixture(6));
 window.showDirectoryPicker=async()=>testDir;
}''')
 source_frame.get_by_role('button',name='Klasörü bağla / izni yenile').click()
 expect(source_frame.locator('#status')).to_contain_text('1 dosya',timeout=30000)
 project_url=source_frame.locator('#projectLink').input_value()
 assert 'pid=' in project_url and 'msid=' not in project_url
 # Viewer is isolated: no directory handle, no previous site permission, no popup allowed.
 panel=browser.new_context(viewport={'width':1440,'height':1000})
 panel.add_init_script("window.folderPickerCalls=0;window.showDirectoryPicker=async()=>{window.folderPickerCalls++;throw new Error('Viewer must not request a local folder')}")
 view=panel.new_page();view.goto(project_url,wait_until='networkidle')
 expect(view.get_by_text('Ortak projede 1 LoggerNet dosyası var.',exact=False)).to_be_visible(timeout=30000)
 vf=view.frame_locator('iframe[title$="maki_browser_loggernet_v1"]')
 vframe=next(f for f in view.frames if 'maki_browser_loggernet_v1' in f.url)
 assert vframe.evaluate('window.folderPickerCalls')==0
 assert vframe.evaluate('handle===null')
 print('PASS isolated viewer loads same project without local folder permission or handle',flush=True)
 frame.evaluate("async()=>{await put('Generic_WindData.dat',fixture(7))}")
 digest=frame.evaluate("async()=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(fixture(7)))),x=>x.toString(16).padStart(2,'0')).join('')")
 frame.wait_for_function("digest=>args.known?.['Generic_WindData.dat']===digest",arg=digest,timeout=35000)
 vframe.wait_for_function("digest=>args.known?.['Generic_WindData.dat']===digest",arg=digest,timeout=35000)
 assert vframe.evaluate('window.folderPickerCalls')==0
 print('PASS automatic source scan propagates new exact SHA256 to separate viewer via server polling',flush=True)
 if os.environ.get('MAKI_LARGE_FIXTURE'):
  data=Path(os.environ['MAKI_LARGE_FIXTURE']).read_bytes()
  frame.evaluate("""async encoded=>{const data=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));const h=await testDir.getFileHandle('Large_WindData.dat',{create:true});const w=await h.createWritable();await w.write(data);await w.close()}""",base64.b64encode(data).decode())
  source_frame.get_by_role('button',name='Şimdi tara').click()
  frame.wait_for_function("digest=>args.known?.['Large_WindData.dat']===digest",arg=hashlib.sha256(data).hexdigest(),timeout=90000)
  vframe.wait_for_function("digest=>args.known?.['Large_WindData.dat']===digest",arg=hashlib.sha256(data).hexdigest(),timeout=45000)
  assert vframe.evaluate('window.folderPickerCalls')==0
  print('PASS large TOA5 reaches second browser byte-exactly without folder access:',len(data),'bytes',flush=True)
 view.reload(wait_until='networkidle')
 expect(view.get_by_text('Ortak projede ',exact=False).first).to_be_visible(timeout=30000)
 vframe=next(f for f in view.frames if 'maki_browser_loggernet_v1' in f.url)
 assert vframe.evaluate('window.folderPickerCalls')==0
 view.get_by_role('button',name='⇧ Veri Yükleme ve Direk Ayarları',exact=False).click()
 view.get_by_text('LoggerNet · Tarayıcıdan otomatik aktarım',exact=False).wait_for(timeout=30000)
 assert view.locator('[data-testid="stException"]').count()==0
 print('PASS viewer refresh/navigation restores shared data and never calls folder picker',flush=True)
 # A different project remains empty; there is no global latest-file fallback.
 other=browser.new_context();empty=other.new_page();empty.goto(URL,wait_until='networkidle')
 expect(empty.get_by_text('Bu projeye henüz veri aktarılmadı.',exact=False)).to_be_visible(timeout=30000)
 print('PASS unrelated project receives no shared measurements',flush=True)
 view.screenshot(path='/tmp/maki_shared_project_v20.png',full_page=True)
 browser.close()
