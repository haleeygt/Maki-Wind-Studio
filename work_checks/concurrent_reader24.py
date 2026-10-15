"""Ensure different cold reads cannot hold parser working memory simultaneously."""
import ast,contextlib,threading,time,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np,pandas as pd,re,streamlit as st
source=Path(__file__).resolve().parents[1]/'appv11.11.25_SABIT_SINIR_RUZGAR_HARITASI.py'
ns={'pd':pd,'np':np,'st':st,'re':re,'__name__':'maki_reader_concurrency_test','RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
for node in ast.parse(source.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in {'_loggernet_okuma_kilidi','loggernet_oku'}:
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),ns)
assert ns['_loggernet_okuma_kilidi']() is ns['_loggernet_okuma_kilidi']()
original=pd.read_csv
active=0;maximum=0;gate=threading.Lock()
@contextlib.contextmanager
def tracked(*args,**kwargs):
 global active,maximum
 with gate:active+=1;maximum=max(maximum,active)
 try:
  time.sleep(.1)
  with original(*args,**kwargs) as reader:yield reader
 finally:
  with gate:active-=1
pd.read_csv=tracked
try:
 start=threading.Barrier(2)
 def read(speed):
  start.wait()
  return ns['loggernet_oku'](f'TIMESTAMP,WS1_Avg\n2025-01-01 00:00:00,{speed}\n'.encode())
 with ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(read,v) for v in [6,7]]
  results=[future.result(timeout=30) for future in futures]
 assert maximum==1,maximum
 assert [float(x.WS1_Avg.iloc[0]) for x in results]==[6,7]
 print('PASS different cold reads are serialized across threads; independent measured values preserved')
finally:pd.read_csv=original
