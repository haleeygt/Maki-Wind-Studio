"""Full page integration using an explicit synthetic raster in place of remote GWA."""
from pathlib import Path
import ast,base64,io,json
import numpy as np,pandas as pd,tifffile
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.26_KARARLILIK_VE_TEMIZ_EKRAN.py'
source=SOURCE.read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_raster_bytes_getir')
buf=io.BytesIO();tifffile.imwrite(buf,np.linspace(5,7,40000,dtype=np.float32).reshape(200,200),extratags=[(33550,'d',3,(.002,.002,0),False),(33922,'d',6,(0,0,0,27.8,41.2,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)])
replacement="def _gwa_raster_bytes_getir(*args, **kwargs):\n    return base64.b64decode("+repr(base64.b64encode(buf.getvalue()).decode())+"), 'SYNTHETIC TEST RASTER', 'test', None\n"
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
assert len(found)==1,[(x.proto.component_name,x.proto.json_args[:100]) for x in components]
args=found[0];assert args['wind'] and args['wind']['matrix']
assert args['polygon']==[[28.,41.],[28.025,41.],[28.025,41.025],[28.,41.025],[28.,41.]]
assert args['wind']['vmin']>0 and args['wind']['vmax']>args['wind']['vmin']
assert len(args['wind']['latitudes'])<=60 and len(args['wind']['longitudes'])<=60
print('PASS complete page passes actual calculated wind grid and unchanged KML boundary to first-tab map (remote raster explicitly replaced by synthetic TIFF)',flush=True)
# A Streamlit component retains its last value across reruns. Consume each drag
# event once, so the Reset button cannot silently replay the previous movement.
map_component=next(x for x in components if 'km' in json.loads(x.proto.json_args))
states=a._tree.get_widget_states()
move=states.widgets.add();move.id=map_component.proto.id
move.json_value=json.dumps({'action':'move','event_id':'test_move_25','lat':41.014,'lon':28.014})
a._run(states);assert not a.exception,a.exception
assert a.session_state['app_state']['wind_map_center']==[41.014,28.014]
a.button(key='big_square_reset').click().run();assert not a.exception,a.exception
assert a.session_state['app_state']['wind_map_center'] is None
print('PASS one drag event updates only the working center; Reset persists across rerun without replaying stale component value',flush=True)
