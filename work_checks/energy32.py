"""Analytic energy/CF and missing-hour bounds, independent of app formulas."""
import ast,datetime,hashlib,json,math,re
from pathlib import Path
from types import SimpleNamespace
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py'
ns={'pd':pd,'np':np,'re':re,'math':math,'datetime':datetime,'st':SimpleNamespace(session_state={}), 'app_state':{},'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
names={'hiz_sensor_kolonlari','olcum_zaman_kontrolu','otomatik_olcum_kontrolu','olcum_kalite_verisi','olcum_kapsama_raporu','enerji_kalite_durumu','enerji_verisi_hesaplanabilir','enerji_shear_hesapla','sensor_yukseklik_tuple','coklu_direk_hub_serisi_hazirla','enerji_yillik_gosterge_ozeti','enerji_girdileri_tutarli','turbin_uretimi_coklu_direk_hesapla'}
for node in ast.parse(SOURCE.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in names:
  node.decorator_list=[];exec(compile(ast.Module(body=[node],type_ignores=[]),str(SOURCE),'exec'),ns)
heights={'WS1_Avg':100,'WS2_Avg':90,'WS3_Avg':80,'WS4_Avg':40}
model={'power_curve':{'wind_speed':[0,6,10,25],'power_kw':[0,600,1000,0]},'nominal_guc_kw':1000}
losses={'wake':12,'availability':5,'electrical':3,'other':4};factor=.7784832
base=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=365*144,freq='10min')})
for c in heights:base[c]=6.
def calculate(frame,loss=None):
 ns['tum_veri_setleri']={'Generic':frame}
 return ns['turbin_uretimi_coklu_direk_hesapla']({'Generic':frame},{'Generic':heights},model,100,3,loss or {})
r=calculate(base,losses);s=r['annual_summary'];expected=5256*3*factor
assert r['annual_ok'] and s['eligible'];assert abs(s['annual_mwh']-expected)<1e-8
assert abs(s['observed_cf_pct']-60*factor)<1e-10 and abs(s['annual_cf_pct']-60*factor)<1e-10
assert s['annual_lower_mwh']==s['annual_upper_mwh']
print('PASS known constant-power 365-day year: exact MWh, multiplicative losses, installed capacity and both CF denominators',flush=True)
gap=base.copy(deep=True);gap.loc[100:256,'WS1_Avg']=np.nan;original=gap.copy(deep=True)
r=calculate(gap,losses);s=r['annual_summary'];missing=157/6
assert not r['annual_ok'] and np.isnan(r['yillik_net_mwh']) and np.isnan(r['kapasite_faktoru'])
assert s['eligible'] and abs(s['annual_mwh']-expected)<1e-8
assert len(r['hesap'])==len(base)-157 and abs(s['missing_hours']-missing)<1e-8
assert abs(r['net_mwh']-(5256-15.7)*3*factor)<1e-8
assert abs(s['period_lower_mwh']-r['net_mwh'])<1e-9
assert abs(s['period_upper_mwh']-(r['net_mwh']+missing*3*factor))<1e-8
assert s['annual_lower_mwh']<=s['annual_mwh']<=s['annual_upper_mwh']
assert any('2 saat' in x for x in r['quality']['Generic']['annual_block_reasons'])
pd.testing.assert_frame_equal(gap,original)
print('PASS 26.17-hour gap: strict annual fields remain blocked; separate conditional equivalent exact; observed rows/raw unchanged; zero-to-rated missing bounds exact',flush=True)
short=base.iloc[:144*20].copy();r=calculate(short);s=r['annual_summary']
assert not s['eligible'] and np.isnan(s['annual_mwh']) and abs(s['observed_cf_pct']-60)<1e-10
no_jan=base.copy();no_jan.loc[no_jan.TIMESTAMP.dt.month.eq(1),'WS1_Avg']=np.nan;r=calculate(no_jan);s=r['annual_summary']
assert not s['eligible'] and np.isnan(s['annual_mwh'])
assert any('12 takvim' in x for x in s['reasons'])
print('PASS short period and missing season cannot produce an annual equivalent; valid-hour CF remains available',flush=True)
leap=pd.DataFrame({'TIMESTAMP':pd.date_range('2024-01-01',periods=366*144,freq='10min')})
for c in heights:leap[c]=6.
r=calculate(leap);s=r['annual_summary'];assert s['valid_hours']==8784
assert abs(r['net_mwh']-8784*.6*3)<1e-8 and abs(s['annual_mwh']-8760*.6*3)<1e-8
print('PASS leap-year observed 8784-hour energy stays distinct from standard 8760-hour annual equivalent',flush=True)
# Seasonal power shape: equal arithmetic mean is wrong for month lengths.
seasonal=base.copy()
for c in heights:seasonal[c]=np.where(seasonal.TIMESTAMP.dt.month.eq(2),10.,6.)
r=calculate(seasonal);s=r['annual_summary'];expected_season=3*((8760-28*24)*.6+28*24*1.)
assert abs(s['annual_mwh']-expected_season)<1e-8
print('PASS monthly seasonal example matches independent month-hour energy integral, not unweighted monthly averaging',flush=True)
# A nonmonotonic power curve must be evaluated at each sample, not at mean wind.
vary=base.copy()
for c in heights:vary[c]=np.where(np.arange(len(vary))%2,0.,20.)
r=calculate(vary);assert abs(r['net_mwh']-8760*3/6)<1e-8
assert abs(r['net_mwh']-8760*3*1.)>1000
print('PASS zero wind remains valid and sample-by-sample power energy agrees with independent two-state expectation',flush=True)

import copy
for bad in [{'wake':-1},{'wake':101},{'wake':np.nan}]:assert calculate(base,bad) is None
for key,value in [('wind_speed',[0,6,6,25]),('power_kw',[0,600,1200,0]),('power_kw',[0,600,np.nan,0])]:
 bad=copy.deepcopy(model);bad['power_curve'][key]=value
 ns['tum_veri_setleri']={'Generic':base}
 assert ns['turbin_uretimi_coklu_direk_hesapla']({'Generic':base},{'Generic':heights},bad,100,3,{}) is None
assert ns['turbin_uretimi_coklu_direk_hesapla']({'Generic':base},{'Generic':heights},model,100,2.5,{}) is None
short=base.iloc[:144].copy();other=short.iloc[::2].copy()
for shifted in [other,short.assign(TIMESTAMP=short.TIMESTAMP+pd.Timedelta(minutes=5))]:
 ns['tum_veri_setleri']={'A':short,'B':shifted}
 assert ns['turbin_uretimi_coklu_direk_hesapla']({'A':short,'B':shifted},{'A':heights,'B':heights},model,100,3,{}) is None
print('PASS malformed/rating-exceeding curves, invalid losses/count, mixed sampling intervals and misaligned stations cannot silently produce energy',flush=True)
