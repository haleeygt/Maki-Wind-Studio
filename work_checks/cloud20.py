"""Shared raw snapshots: isolation, update propagation and settings concurrency."""
import ast, base64, datetime, hashlib, json, os, re, tempfile, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'appv11.11.28_CALISMA_KARESINDE_RUZGAR_HARITASI.py'
tree=ast.parse(SOURCE.read_text())
names={'_loggernet_oku_dogrudan','_loggernet_cache_dizini','_loggernet_okuma_kilidi','_bulut_proje_dizini','_bulut_manifest_oku','_bulut_manifest_yaz','_bulut_kayitlari',
'bulut_loggernet_yayinla','bulut_proje_ayarlarini_esitle','bulut_proje_verisini_al',
'loggernet_oku','tarayici_loggernet_kaydini_hazirla','tarayici_loggernet_kaydini_uygula'}
lock=threading.RLock()
def browser(folder,pid):
 ns={'__file__':str(folder/'app.py'),'Path':Path,'re':re,'json':json,'uuid':uuid,'os':os,
     'datetime':datetime,'hashlib':hashlib,'base64':base64,'np':np,'pd':pd,
     '_BULUT_PROJE_ID':pid,'_bulut_proje_kilidi':lambda:lock,
     'BULUT_ORTAK_ALANLAR':('sensor_heights','mast_registry','mast_coordinates','quality_flags'),
     'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg'],
     'st':SimpleNamespace(session_state={}),
     'app_state':{'wind_data_files':[],'data_source':'LoggerNet klasörü',
                  'sensor_heights':{},'mast_registry':{},'mast_coordinates':{},'quality_flags':{}}}
 for n in tree.body:
  if isinstance(n,ast.FunctionDef) and n.name in names:
   n.decorator_list=[];exec(compile(ast.Module(body=[n],type_ignores=[]),str(SOURCE),'exec'),ns)
 return ns
folder_id=str(uuid.uuid4())
def event(name='Alpha_WindData.dat',speed=6):
 q=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=8,freq='10min'),
                 'WS1_Avg':speed,'WS2_Avg':5.8})
 raw=q.to_csv(index=False).encode()
 return {'action':'file','name':name,'folder_id':folder_id,'size':len(raw),'mtime_ms':1735689600000,
         'sha256':hashlib.sha256(raw).hexdigest(),'base64':base64.b64encode(raw).decode()}
with tempfile.TemporaryDirectory(prefix='maki_project_test_') as tmp:
 folder=Path(tmp);pid=uuid.uuid4().hex+uuid.uuid4().hex
 a,b=browser(folder,pid),browser(folder,pid)
 c=browser(folder,uuid.uuid4().hex+uuid.uuid4().hex)
 first=event();a['tarayici_loggernet_kaydini_uygula'](first)
 a['app_state']['sensor_heights']={'Alpha_WindData.dat':{'WS1_Avg':81,'WS2_Avg':77}}
 a['bulut_proje_verisini_al']()
 b['bulut_proje_verisini_al']()
 assert b['app_state']['sensor_heights']==a['app_state']['sensor_heights']
 files=b['app_state']['wind_data_files']
 assert len(files)==1 and 'bytes' not in files[0]
 assert Path(files[0]['source_path']).read_bytes()==base64.b64decode(first['base64'])
 print('PASS second browser reads byte-exact cloud snapshot and sensor heights without folder permission')
 c['bulut_proje_verisini_al']();assert not c['app_state']['wind_data_files']
 print('PASS independent project sees no other project data')
 # Reviewer marks a sensor; source browser's subsequent upload must retain those marks.
 key='qc_flags_Direk 1 · Alpha_WindData.dat_WS1_Avg'
 b['app_state']['quality_flags']={key:[{'from':'2025-01-01','to':'2025-01-01 00:10','reason':'test'}]}
 b['bulut_proje_ayarlarini_esitle'](b['app_state'])
 second=event(speed=7);a['tarayici_loggernet_kaydini_uygula'](second)
 a['bulut_proje_verisini_al']();b['bulut_proje_verisini_al']()
 assert key in a['st'].session_state and key in b['st'].session_state
 assert Path(b['app_state']['wind_data_files'][0]['source_path']).read_bytes()==base64.b64decode(second['base64'])
 assert len(list((folder/'.maki_runtime/cloud_projects'/pid).glob('*.dat')))==2
 print('PASS source update propagates; shared QC flags retained; in-flight prior snapshot kept')
 # New mast is appended, never reorders existing quality keys.
 a['tarayici_loggernet_kaydini_uygula'](event('Aardvark_WindData.dat'))
 b['bulut_proje_verisini_al']()
 assert [x['name'] for x in b['app_state']['wind_data_files']]==['Alpha_WindData.dat','Aardvark_WindData.dat']
 print('PASS new mast does not reorder existing mast identities')
 # Independent field changes merge rather than clobbering an entire stale project.
 a['app_state']['mast_coordinates']={'Alpha_WindData.dat':[40.1,28.2]}
 a['bulut_proje_ayarlarini_esitle'](a['app_state'])
 b['app_state']['sensor_heights']['Alpha_WindData.dat']['WS1_Avg']=82
 b['bulut_proje_ayarlarini_esitle'](b['app_state'])
 a['bulut_proje_verisini_al']()
 assert a['app_state']['sensor_heights']['Alpha_WindData.dat']['WS1_Avg']==82
 assert b['app_state']['mast_coordinates']==a['app_state']['mast_coordinates']
 print('PASS concurrent changes to different metadata fields merge')
 before=Path(b['app_state']['wind_data_files'][0]['source_path']).read_bytes()
 bad={**event(),'sha256':'0'*64}
 try:a['tarayici_loggernet_kaydini_uygula'](bad)
 except ValueError:pass
 else:raise AssertionError('Bad snapshot accepted')
 b['bulut_proje_verisini_al']()
 assert Path(b['app_state']['wind_data_files'][0]['source_path']).read_bytes()==before
 print('PASS corrupt upload never becomes a shared snapshot')
 b['app_state']['data_source']='Manuel dosya yükleme'
 b['app_state']['wind_data_files']=[{'name':'local.csv','bytes':b'manual'}]
 b['bulut_proje_verisini_al']()
 assert b['app_state']['wind_data_files'][0]['bytes']==b'manual'
 print('PASS manually loaded work is not overwritten by shared data')
 # New source process can restore snapshots from disk after losing Python session state.
 restored=browser(folder,pid);restored['bulut_proje_verisini_al']()
 assert len(restored['app_state']['wind_data_files'])==2
 print('PASS fresh Python session restores existing project snapshots')
