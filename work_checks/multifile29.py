"""Five independent test datasets: compare retained tables with on-demand loading."""
import ast,json,math,os,re,resource,subprocess,sys,tempfile,weakref
from pathlib import Path
import numpy as np,pandas as pd,streamlit as st
ROOT=Path(__file__).resolve().parents[1]
NEW=ROOT/'appv11.11.29_COKLU_DOSYA_BELLEK_KONTROLU.py'
OLD=ROOT/'previous_versions/appv11.11.28_CALISMA_KARESINDE_RUZGAR_HARITASI.py'
fixture=os.environ.get('MAKI_LARGE_FIXTURE')
if '--worker' not in sys.argv:
 if not fixture:raise SystemExit('Set MAKI_LARGE_FIXTURE; test requires real fixture')
 results=[]
 for mode in ['old','new']:
  p=subprocess.run([sys.executable,__file__,'--worker',mode],capture_output=True,text=True,check=True)
  results.append(json.loads(p.stdout.strip().splitlines()[-1]))
 before,after=results
 assert after['digests']==before['digests'] and after['quality']==before['quality']
 assert after['peak_mib']<before['peak_mib']*.9,results
 print('PASS five independent datasets: identical table digests and all quality summaries; peak MiB',round(before['peak_mib'],1),'->',round(after['peak_mib'],1),flush=True)
 raise SystemExit(0)
mode=sys.argv[-1];source=OLD if mode=='old' else NEW
ns={'np':np,'pd':pd,'st':st,'math':math,'re':re,'Path':Path,'__file__':str(source),'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
names={'_loggernet_okuma_kilidi','_loggernet_cache_dizini','loggernet_oku','_loggernet_oku_dogrudan','hiz_sensor_kolonlari','olcum_zaman_kontrolu','otomatik_olcum_kontrolu','LoggerNetVeriSetleri'}
for n in ast.parse(source.read_text()).body:
 if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:exec(compile(ast.Module(body=[n],type_ignores=[]),str(source),'exec'),ns)
raw=Path(fixture).read_bytes();original=ns['loggernet_oku']
# Explicit test-only variation gives five independent QA/cache keys, without private files in git.
def varied(content):
 f=original(raw);i=len(content)-len(raw);f['WS1_Avg']=f['WS1_Avg']+i*.001
 return f
ns['loggernet_oku']=varied
class File:
 def __init__(self,i):self.i=i
 def getvalue(self):return raw+b'\n'*self.i
files=[File(i) for i in range(5)];tables={} if mode=='old' else ns['LoggerNetVeriSetleri']()
digests=[];quality=[]
for i,file in enumerate(files):
 frame=varied(file.getvalue());out=ns['otomatik_olcum_kontrolu'](frame)
 digests.append(str(pd.util.hash_pandas_object(frame,index=True).sum()))
 quality.append([len(frame),len(out[2]),out[3]])
 if mode=='old':tables[i]=frame
 else:tables.kaydet(i,file)
 del frame,out
for i in range(5):
 f=tables[i];assert str(pd.util.hash_pandas_object(f,index=True).sum())==digests[i]
 if mode=='new' and i:
  assert previous() is None,'Inactive dataset retained in collection'
 previous=weakref.ref(f);del f
assert len(tables)==5 and list(tables.keys())==list(range(5))
assert tables.get('missing') is None
print(json.dumps({'mode':mode,'digests':digests,'quality':quality,'peak_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}))
