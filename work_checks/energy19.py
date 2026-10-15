"""No user approval gate; preserve cleaning, cadence, shear and annual coverage limits."""
import ast, datetime, hashlib, json, math, re
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'appv11.11.31_TURBIN_RUZGAR_KATMANI_DUZELTMESI.py'
ns={'pd':pd,'np':np,'re':re,'hashlib':hashlib,'json':json,'math':math,'datetime':datetime,
    'st':SimpleNamespace(session_state={}), 'app_state':{},
    'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
names={'hiz_sensor_kolonlari','olcum_zaman_kontrolu','otomatik_olcum_kontrolu',
'olcum_kalite_verisi','olcum_kapsama_raporu','enerji_kalite_durumu',
'enerji_verisi_hesaplanabilir','enerji_shear_hesapla','sensor_yukseklik_tuple',
'coklu_direk_hub_serisi_hazirla','turbin_uretimi_coklu_direk_hesapla'}
for node in ast.parse(p.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in names:
  node.decorator_list=[]
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),ns)
year=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=365*144,freq='10min')})
for c in ns['RUZGAR_KOLONLARI']:year[c]=6.
raw=year.copy(deep=True)
heights=dict(zip(ns['RUZGAR_KOLONLARI'],[102.,98.,80.,40.]))
model={'power_curve':{'wind_speed':[0,6,10,25],'power_kw':[0,600,1000,0]},'nominal_guc_kw':1000}
ns['tum_veri_setleri']={'Mast':year}
calc=ns['turbin_uretimi_coklu_direk_hesapla']
r=calc({'Mast':year},{'Mast':heights},model,102,1,{'loss':0})
assert r and r['annual_ok'] and abs(r['yillik_net_mwh']-5256)<1e-8
assert 'quality_approvals' not in ns['app_state']
print('PASS energy calculates without review record; annual result 5256 MWh; no fake approval created')
ns['st'].session_state['qc_flags_Mast_WS1_Avg']=[{'from':str(year.TIMESTAMP.iloc[100]),'to':str(year.TIMESTAMP.iloc[117]),'reason':'test'}]
r=calc({'Mast':year},{'Mast':heights},model,102,1,{'loss':0})
assert r and not r['annual_ok'] and np.isnan(r['yillik_net_mwh'])
assert abs(r['net_mwh']-(len(year)-18)*.1)<1e-8
pd.testing.assert_frame_equal(year,raw)
print('PASS manual flags excluded; raw unchanged; 3-hour gap suppresses annual output; original energy timestep retained')
ns['st'].session_state.clear()
dup=year.copy();dup.loc[1,'TIMESTAMP']=dup.loc[0,'TIMESTAMP'];ns['tum_veri_setleri']={'Mast':dup}
assert calc({'Mast':dup},{'Mast':heights},model,102,1,{}) is None
empty=year.copy();empty.WS1_Avg=np.nan;ns['tum_veri_setleri']={'Mast':empty}
assert calc({'Mast':empty},{'Mast':heights},model,102,1,{}) is None
solo=year[['TIMESTAMP','WS1_Avg']].copy();ns['tum_veri_setleri']={'Mast':solo}
assert calc({'Mast':solo},{'Mast':{'WS1_Avg':102}},model,120,1,{}) is None
assert calc({'Mast':solo},{'Mast':{'WS1_Avg':102}},model,102,1,{}) is not None
print('PASS duplicate timestamps/empty reference block energy; unavailable shear blocks hub conversion; direct-height energy remains available')
