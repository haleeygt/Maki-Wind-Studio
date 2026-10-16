"""A full-year gap, current loss selection and actual manual turbine count in the UI."""
from pathlib import Path
import ast,base64,io
import numpy as np,pandas as pd,tifffile
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py'
source=SOURCE.read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_raster_bytes_getir')
buf=io.BytesIO();tifffile.imwrite(buf,np.full((100,100),6,dtype=np.float32),extratags=[(33550,'d',3,(.004,.004,0),False),(33922,'d',6,(0,0,0,27.8,41.2,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)])
replacement="def _gwa_raster_bytes_getir(*args, **kwargs):\n    return base64.b64decode("+repr(base64.b64encode(buf.getvalue()).decode())+"), 'SYNTHETIC TEST RASTER', 'test', None\n"
lines=source.splitlines(True);lines[node.lineno-1:node.end_lineno]=[replacement];source=''.join(lines)
a=AppTest.from_string(source,default_timeout=90).run();assert not a.exception
frame=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=8760,freq='h')})
for c in ['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']:frame[c]=6.
frame['WD1_Avg']=200;frame['WD2_Avg']=210;frame.loc[100:125,'WS1_Avg']=np.nan
state=a.session_state['app_state'];state['data_source']='Manuel dosya yükleme'
state['wind_data_files']=[{'name':'Generic.csv','bytes':frame.to_csv(index=False).encode()}]
state['sensor_heights']={'Generic.csv':{'WS1_Avg':100,'WS2_Avg':90,'WS3_Avg':80,'WS4_Avg':40}}
state['santral_boundary']={'name':'Generic.kml','bytes':b'<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark><Polygon><outerBoundaryIs><LinearRing><coordinates>28,41 28.025,41 28.025,41.025 28,41.025 28,41</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark></kml>'}
state['micrositing_topography_ready']=True;state['turbine_count']=7;state['hub_height']=100
state['turbine_placement_mode']='Manuel / Excel yerleşimi'
state['manual_turbine_points']=[{'lat':41.003+i%5*.003,'lon':28.003+i//5*.003,'ad':f'T{i+1}'} for i in range(17)]
for k,v in [('direk_kullan_1',True),('direk_lat_1',41.012),('direk_lon_1',28.012)]:a.session_state[k]=v
a.sidebar.button(key='v8_nav_Üretim Hesaplama').click().run();assert not a.exception,a.exception
# Change scenario once: header must immediately agree with the recomputed metrics.
a.selectbox(key='uretim_kayip_senaryosu_widget').set_value('P90').run();assert not a.exception,a.exception
metrics={x.label:x.value for x in a.metric}
annual_label=next(k for k in metrics if k.startswith('Yıllık net eşdeğer'))
assert 'Eksik saat varsayımıyla' in annual_label
factor=.7784832;annual=1417*17*8760*factor/1000
expected_cf=1417/8000*factor*100
assert metrics[annual_label]==f'{annual:,.0f} MWh/yıl',(metrics,annual)
assert metrics['Yıllık eşdeğer net kapasite faktörü']==f'%{expected_cf:.1f}'
assert metrics['Kurulu güç']=='136.0 MW'
assert metrics['Eksik / dışlanan saat']=='26.0 saat'
assert metrics['Geçerli kayıtlardan net enerji tahmini']==f'{1417*17*(8760-26)*factor/1000:,.0f} MWh'
headers=[x.value for x in a.info if 'Saha:' in x.value]
assert len(headers)==1 and '17 türbin' in headers[0] and '136.0 MW' in headers[0] and 'Yüksek kayıp varsayımı' in headers[0],headers
assert not any('Senaryo: P50' in x for x in headers)
assert any('yatırım kararı' in x.value for x in a.warning)
assert any('aynı ayın' in x.value for x in a.warning)
assert any('26.00 saat' in x.value and '2 saat' in x.value for x in a.caption)
assert not any(x.value=='Hesaplanmadı' for x in a.metric)
print('PASS full UI: 26-hour gap has separate conditional annual/CF, observed energy and hours; warning, current scenario and actual 17 turbines/136 MW agree',flush=True)
# A short selected period keeps observable CF but must not show a spurious annual value.
state=a.session_state['app_state'];state['date_start']=pd.Timestamp('2025-01-01').date();state['date_end']=pd.Timestamp('2025-01-20').date()
a.run();assert not a.exception,a.exception
metrics={x.label:x.value for x in a.metric}
assert metrics['Yıllık net eşdeğer']=='Veri yetersiz'
assert metrics['Net kapasite faktörü · geçerli saatler'].startswith('%')
print('PASS short-period UI refuses annual equivalent but retains correctly labeled observed-hour CF',flush=True)
