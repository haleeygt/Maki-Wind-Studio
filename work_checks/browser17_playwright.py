from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import os,base64
import hashlib
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1500,'height':1100})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('MAKI_TEST_URL','http://127.0.0.1:8507'),wait_until='networkidle')
 page.get_by_role('button',name='⇧ Veri Yükleme ve Direk Ayarları',exact=False).click()
 page.get_by_text('LoggerNet bağlantısı · v11.11.17',exact=True).wait_for()
 frame=page.frame_locator('iframe[title$="maki_browser_loggernet_v1"]')
 if not frame.get_by_role('button',name='Klasörü bağla / izni yenile').is_visible():
  page.get_by_text('LoggerNet otomatik bağlantı',exact=True).click()
 frame.get_by_role('button',name='Klasörü bağla / izni yenile').wait_for(timeout=30000)
 iframe=next(f for f in page.frames if 'maki_browser_loggernet_v1' in f.url)
 print('Native folder API:',iframe.evaluate("({secure:isSecureContext,picker:typeof showDirectoryPicker,origin:location.origin})"),flush=True)
 # Real browser file/directory handles in OPFS; only the native picker dialog is substituted.
 print('Preparing sandbox folder',flush=True)
 iframe.evaluate('''async()=>{
 const root=await navigator.storage.getDirectory();
 window.testDir=await root.getDirectoryHandle('loggernet-test',{create:true});
 window.fixture=n=>['TIMESTAMP,WS1_Avg,WS2_Avg,WS3_Avg,WS4_Avg',...Array.from({length:n},(_,i)=>`2025-01-01 00:${String(i*10).padStart(2,'0')}:00,6,5.8,5.5,5`)].join('\\n')+'\\n';
 window.put=async(name,text)=>{let h=await testDir.getFileHandle(name,{create:true});let w=await h.createWritable();await w.write(text);await w.close()};
 await put('Project_A_WindData.dat',fixture(3));
 await put('Ignore_RawData.dat',fixture(3));
 await put('Other.csv',fixture(3));
 window.showDirectoryPicker=async()=>testDir;
}''')
 frame.get_by_role('button',name='Klasörü bağla / izni yenile').click()
 page.get_by_text('LoggerNet bağlantısı · v11.11.17',exact=True).wait_for(timeout=30000)
 expect(page.get_by_test_id('stMetricValue').filter(has_text='1').first).to_be_visible(timeout=30000)
 expect(frame.locator('#status')).to_contain_text('1 dosya',timeout=30000)
 print('Initial automatic import PASS',flush=True)
 page.get_by_role('button',name='⇧ Veri Yükleme ve Direk Ayarları',exact=False).click()
 page.get_by_text('LoggerNet · Tarayıcıdan otomatik aktarım',exact=False).wait_for()
 assert page.locator('[data-testid="stException"]').count()==0
 iframe=next(f for f in page.frames if 'maki_browser_loggernet_v1' in f.url)
 iframe.evaluate("async()=>{await put('Project_A_WindData.dat',fixture(4))}")
 # Require server ACK for the new exact byte digest, not the previous status text.
 expected=iframe.evaluate("async()=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(fixture(4)))),x=>x.toString(16).padStart(2,'0')).join('')")
 iframe.wait_for_function("(digest)=>args.known?.['Project_A_WindData.dat']===digest",arg=expected,timeout=35000)
 print('PASS scheduled scan uploaded modified bytes; exact server-acknowledged SHA256 matches',flush=True)
 # Incomplete tail must not replace previously accepted data.
 iframe.evaluate("async()=>{await put('Project_A_WindData.dat',fixture(4).slice(0,-1))}")
 frame.get_by_role('button',name='Şimdi tara').click()
 expect(frame.locator('#status')).to_contain_text('son satır tamamlanmamış',timeout=20000)
 iframe.wait_for_function("()=>!busy",timeout=15000)
 iframe.wait_for_function("(digest)=>args.known?.['Project_A_WindData.dat']===digest",arg=expected,timeout=15000)
 print('PASS incomplete tail preserves accepted snapshot',flush=True)
 if os.environ.get('MAKI_LARGE_FIXTURE'):
  raw=Path(os.environ['MAKI_LARGE_FIXTURE']).read_bytes()
  iframe=next(f for f in page.frames if 'maki_browser_loggernet_v1' in f.url)
  iframe.evaluate("""async encoded=>{const data=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));let h=await testDir.getFileHandle('Sample_WindData.dat',{create:true});let w=await h.createWritable();await w.write(data);await w.close()}""",base64.b64encode(raw).decode())
  frame.get_by_role('button',name='Şimdi tara').click()
  iframe.wait_for_function("digest=>args.known?.['Sample_WindData.dat']===digest",arg=hashlib.sha256(raw).hexdigest(),timeout=60000)
  print('PASS full TOA5 fixture transported and acknowledged byte-for-byte:',len(raw),'bytes',flush=True)
 frame.get_by_role('button',name='Takibi durdur').click()
 page.get_by_role('button',name='Devam et · Rüzgâr Kaynağı Özeti',exact=False).click()
 expect(frame.locator('#status')).to_contain_text('Otomatik takip durduruldu',timeout=30000)
 page.get_by_text('Ham Veri',exact=True).wait_for(timeout=30000)
 assert page.locator('[data-testid="stException"]').count()==0
 page.screenshot(path=str(Path('/tmp')/'maki_browser_folder_v17.png'),full_page=True)
 print('PASS folder bridge survives page navigation and respects paused tracking',flush=True)
 print('Updated automatically; analysis route no exception; browser errors:',errors,flush=True)
 b.close()
