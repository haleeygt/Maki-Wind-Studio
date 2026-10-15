"""Full page integration using an explicit synthetic raster in place of remote GWA."""
from pathlib import Path
import ast,base64,io,json
import numpy as np,pandas as pd,tifffile
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.31_TURBIN_RUZGAR_KATMANI_DUZELTMESI.py'
source=SOURCE.read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_raster_bytes_getir')
buf=io.BytesIO();tifffile.imwrite(buf,np.linspace(5,7,40000,dtype=np.float32).reshape(200,200),extratags=[(33550,'d',3,(.002,.002,0),False),(33922,'d',6,(0,0,0,27.8,41.2,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)])
replacement="def _gwa_raster_bytes_getir(*args, **kwargs):\n    raise RuntimeError('TEST_RASTER_MEMORY_LIMIT: raster parçası bellek sınırını aşıyor')\n"
lines=source.splitlines(True);lines[node.lineno-1:node.end_lineno]=[replacement];source=''.join(lines)
a=AppTest.from_string(source,default_timeout=60).run();assert not a.exception,a.exception
frame=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=144,freq='10min')})
for i,speed in enumerate([6,5.8,5.5,5],1):frame[f'WS{i}_Avg']=speed+np.sin(np.arange(144)/12)*.5
frame['WD1_Avg']=200;frame['WD2_Avg']=210
state=a.session_state['app_state'];state['data_source']='Manuel dosya yükleme'
state['wind_data_files']=[{'name':'Generic_Mast.csv','bytes':frame.to_csv(index=False).encode()}]
state['sensor_heights']={'Generic_Mast.csv':dict(zip(['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg'],[83,78.5,60,40]))}
kml=b'<kml xmlns="http://www.opengis.net/kml/2.2"><Placemark><Polygon><outerBoundaryIs><LinearRing><coordinates>28,41 28.025,41 28.025,41.025 28,41.025 28,41</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark></kml>'
state['santral_boundary']={'name':'Generic.kml','bytes':kml};state['micrositing_topography_ready']=True
state['turbine_count']=1
for key,value in [('direk_kullan_1',True),('direk_lat_1',41.012),('direk_lon_1',28.012)]:a.session_state[key]=value
a.sidebar.button(key='v8_nav_Üretim Hesaplama').click().run();assert not a.exception,a.exception
components=a.get('component_instance')
found=[]
for component in components:
 args=json.loads(component.proto.json_args)
 if 'wind' in args and 'km' in args:found.append(args)
assert len(found)==1
assert found[0]['wind'] is None
assert found[0]['polygon']
assert any('TEST_RASTER_MEMORY_LIMIT' in error.value for error in a.error)
assert not any('Header satırı sabit' in element.value for element in a.markdown)
a.sidebar.button(key='v8_nav_Rüzgar Kaynağı Özeti').click().run()
assert not a.exception,a.exception
assert a.session_state['app_state']['active_page']=='Rüzgar Kaynağı Özeti'
print('PASS bounded raster failure leaves boundary visible, explains the error and permits navigation; no leaked technical text',flush=True)
