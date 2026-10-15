"""Compare reader outputs and isolated-process peak memory; no private fixture in git."""
import ast,json,os,re,subprocess,sys,warnings
from pathlib import Path
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'previous_versions/appv11.11.23_TARAYICI_AKISINA_DONUS.py'
NEW=ROOT/'appv11.11.25_SABIT_SINIR_RUZGAR_HARITASI.py'
warnings.filterwarnings('ignore',category=UserWarning)
def reader(path):
 ns={'np':np,'pd':pd,'re':re,'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
 tree=ast.parse(path.read_text())
 for n in tree.body:
  if isinstance(n,ast.FunctionDef) and n.name in {'_loggernet_okuma_kilidi','loggernet_oku'}:
   n.decorator_list=[]
   exec(compile(ast.Module(body=[n],type_ignores=[]),str(path),'exec'),ns)
 return ns['loggernet_oku']
if '--measure' in sys.argv:
 import resource,hashlib
 fn=reader(Path(sys.argv[2]));data=Path(sys.argv[3]).read_bytes();result=fn(data)
 print(json.dumps({'rows':len(result),'peak_mb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
  'frame_digest':hashlib.sha256(pd.util.hash_pandas_object(result,index=True).values.tobytes()).hexdigest(),
  'attrs':result.attrs}))
 raise SystemExit(0)
a,b=reader(OLD),reader(NEW)
count=0
for sep in [',',';','\t']:
 for newline in ['\n','\r\n']:
  for header in ['TIMESTAMP','DateTime','timestamp']:
   rows=[sep.join([header,'WS1_Avg','WS2_Avg','RECORD'])]+[sep.join([str(pd.Timestamp('2025-01-01')+pd.Timedelta(minutes=10*i)),str(v),str(v*1.23456789),str(i)]) for i,v in enumerate(np.random.default_rng(9).uniform(0,25,8201))]
   for invalid in [False,True]:
    if invalid:rows[4102]=sep.join(['bad-time','bad-number','',''])
    raw=('\ufeff'+newline.join(rows)+newline).encode()
    x,y=a(raw),b(raw);assert_frame_equal(x,y,check_exact=True);assert x.attrs==y.attrs
    count+=1
print(f'PASS {count} CSV variants exactly preserve values, dtypes, timestamps and invalid-time metadata across chunk boundaries',flush=True)
fixture=os.environ.get('MAKI_LARGE_FIXTURE')
if fixture:
 measured=[]
 for path in [OLD,NEW]:
  completed=subprocess.run([sys.executable,__file__,'--measure',str(path),fixture],check=True,capture_output=True,text=True)
  measured.append(json.loads(completed.stdout))
 before,after=measured
 assert before['frame_digest']==after['frame_digest'] and before['attrs']==after['attrs']
 assert before['rows']==after['rows']
 assert after['peak_mb'] < before['peak_mb']*.75,(before,after)
 print('PASS real LoggerNet snapshot exact equality:',after['rows'],'rows',flush=True)
 print('PASS isolated reader peak memory MB:',round(before['peak_mb'],1),'->',round(after['peak_mb'],1),flush=True)
else:print('SKIP real-file memory/equivalence check: set MAKI_LARGE_FIXTURE',flush=True)
