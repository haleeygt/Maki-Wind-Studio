"""Exercise the real HTTP service and stdlib sender without Chrome or FSA."""
from pathlib import Path
import ast, hashlib, importlib.machinery, importlib.util, json, os, shutil, sys, urllib.error, urllib.request, uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from maki_transfer import ProjectStore, loggernet_oku
BASE = os.environ.get('MAKI_TEST_URL', 'http://127.0.0.1:8510')
pid = uuid.uuid4().hex + uuid.uuid4().hex
store = ProjectStore(pid)
root = store._bulut_proje_dizini(); root.mkdir(parents=True)
store._bulut_manifest_yaz({'schema':1, 'files':[], 'settings':{'quality_flags':{'keep':[3]}}})
source = Path('/tmp') / ('maki-sender-test-' + uuid.uuid4().hex);source.mkdir()
loader = importlib.machinery.SourceFileLoader('sender21', str(Path(__file__).resolve().parents[1] / 'maki_loggernet_yardimci.pyw'))
spec = importlib.util.spec_from_loader(loader.name, loader);sender = importlib.util.module_from_spec(spec);loader.exec_module(sender)
# Only the test replaces HTTPS validation for loopback. Production never disables TLS.
try:
 sender.connection('http://example.org/?pid='+pid)
 raise AssertionError('Plain HTTP accepted')
except ValueError: pass
sender.connection=lambda url: (BASE,pid)
config={'url':'test-only','folder':str(source),'folder_id':str(uuid.uuid4())}
def raw(path, data=None, metadata=None, auth=pid):
 headers={'Authorization':'Bearer '+auth}
 if metadata: headers['X-Maki-Metadata']=json.dumps(metadata)
 req=urllib.request.Request(BASE+'/maki-sync/v1/'+path, data=data, headers=headers)
 try:
  with urllib.request.urlopen(req, timeout=180) as res:return res.status,json.loads(res.read())
 except urllib.error.HTTPError as error:return error.code,json.loads(error.read())
fixture=b'TIMESTAMP,WS1_Avg,WS2_Avg\n2025-01-01 00:00:00,6.2,6.0\n2025-01-01 00:10:00,6.4,6.2\n'
try:
 assert raw('status',auth='bad')[0]==401
 assert raw('status',auth=uuid.uuid4().hex*2)[0]==401
 print('PASS malformed/unknown project cannot read or upload',flush=True)
 (source/'Generic_WindData.dat').write_bytes(fixture)
 (source/'ignored_RawData.dat').write_bytes(fixture)
 assert sender.scan(config)==1
 assert sender.scan(config)==0
 manifest=store._bulut_manifest_oku();item=manifest['files'][0]
 assert store._bulut_kayitlari(manifest)[0]['name']=='Generic_WindData.dat'
 assert (root/(item['sha256']+'.dat')).read_bytes()==fixture
 assert manifest['settings']['quality_flags']=={'keep':[3]}
 print('PASS Chrome-free sender publishes exact bytes, retains quality flags, skips unchanged/RawData',flush=True)
 meta={k:item[k] for k in ('name','sha256','size','mtime_ms','folder_id')}
 revision=manifest['revision']
 for data,metadata in [(fixture[:-1],meta),(b'x'*len(fixture),meta),(fixture,{**meta,'name':'../WindData.dat'}),(fixture,{**meta,'size':True}),(fixture,{**meta,'folder_id':str(uuid.uuid4())})]:
  assert raw('file',data,metadata)[0]==400
  assert store._bulut_manifest_oku()['revision']==revision
 print('PASS truncated, corrupt, traversal, invalid size and different-folder uploads preserve prior snapshot',flush=True)
 (root/(item['sha256']+'.dat')).unlink()
 assert raw('status')[1]['known']=={}
 assert sender.scan(config)==1
 print('PASS sender repairs missing server snapshot from unchanged source file',flush=True)
 # A writer's incomplete final line is left alone until completed.
 (source/'Generic_WindData.dat').write_bytes(fixture+b'2025-01-01 00:20:00,7,7')
 assert sender.scan(config)==0
 (source/'Generic_WindData.dat').write_bytes(fixture+b'2025-01-01 00:20:00,7,7\n')
 assert sender.scan(config)==1
 print('PASS unfinished final row waits; completed new measurement uploads automatically',flush=True)
 if os.environ.get('MAKI_LARGE_FIXTURE'):
  original=Path(os.environ['MAKI_LARGE_FIXTURE']).read_bytes()
  (source/'Large_WindData.dat').write_bytes(original)
  assert sender.scan(config)==1
  item=next(x for x in store._bulut_manifest_oku()['files'] if x['name']=='Large_WindData.dat')
  assert (root/(item['sha256']+'.dat')).read_bytes()==original
  print('PASS real LoggerNet file: '+str(len(original))+' bytes, SHA256 identical',flush=True)
 app=ast.parse(Path('appv11.11.22_YENI_BULUT_BAGLANTISI.py').read_text())
 module=ast.parse(Path('maki_transfer.py').read_text())
 a=next(n for n in app.body if isinstance(n,ast.FunctionDef) and n.name=='loggernet_oku');a.decorator_list=[]
 b=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='loggernet_oku')
 assert ast.dump(a)==ast.dump(b)
 print('PASS HTTP and UI use equivalent unchanged LoggerNet parser',flush=True)
finally:
 shutil.rmtree(root);shutil.rmtree(source)
