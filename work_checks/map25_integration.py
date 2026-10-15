"""Full page integration using an explicit synthetic raster in place of remote GWA."""
from pathlib import Path
import ast,base64,io,json
import numpy as np,pandas as pd,tifffile
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.28_CALISMA_KARESINDE_RUZGAR_HARITASI.py'
source=SOURCE.read_text();node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_raster_bytes_getir')
buf=io.BytesIO();tifffile.imwrite(buf,np.linspace(5,7,40000,dtype=np.float32).reshape(200,200),extratags=[(33550,'d',3,(.004,.004,0),False),(33922,'d',6,(0,0,0,27.6,41.4,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)])
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
state['wind_map_center']=[41.04,28.04]
for key,value in [('direk_kullan_1',True),('direk_lat_1',41.012),('direk_lon_1',28.012)]:a.session_state[key]=value
a.sidebar.button(key='v8_nav_Üretim Hesaplama').click().run();assert not a.exception,a.exception
components=a.get('component_instance')
found=[]
for component in components:
 args=json.loads(component.proto.json_args)
 if 'wind' in args and 'km' in args:found.append(args)
assert len(found)==1,[(x.proto.component_name,x.proto.json_args[:100]) for x in components]
args=found[0];assert args['wind'] and args['wind']['matrix']
initial_scale=dict(args['wind']['scale']);assert initial_scale['scope']=='santral'
initial_range=(args['wind']['vmin'],args['wind']['vmax'])
assert args['polygon']==[[28.,41.],[28.025,41.],[28.025,41.025],[28.,41.025],[28.,41.]]
assert args['wind']['vmin']>0 and args['wind']['vmax']>args['wind']['vmin']
assert len(args['wind']['latitudes'])<=60 and len(args['wind']['longitudes'])<=60
print('PASS complete page passes actual calculated wind grid and unchanged KML boundary to first-tab map (remote raster explicitly replaced by synthetic TIFF)',flush=True)
# A Streamlit component retains its last value across reruns. Consume each drag
# event once, so the Reset button cannot silently replay the previous movement.
map_component=next(x for x in components if 'km' in json.loads(x.proto.json_args))
states=a._tree.get_widget_states()
move=states.widgets.add();move.id=map_component.proto.id
move.json_value=json.dumps({'action':'move','event_id':'test_move_25','lat':41.0125,'lon':28.0125})
a._run(states);assert not a.exception,a.exception
assert a.session_state['app_state']['wind_map_center']==[41.0125,28.0125]
moved_args=next(json.loads(x.proto.json_args) for x in a.get('component_instance') if 'km' in json.loads(x.proto.json_args))
assert moved_args['wind']['scale']==initial_scale
assert (moved_args['wind']['vmin'],moved_args['wind']['vmax'])==initial_range
assert not any('Header satırı sabit' in element.value for element in a.markdown)
print('PASS moving working-area center from outside to plant center preserves exact color reference and limits; no technical text leak',flush=True)
a.button(key='big_square_reset').click().run();assert not a.exception,a.exception
assert a.session_state['app_state']['wind_map_center'] is None
reset_args=next(json.loads(x.proto.json_args) for x in a.get('component_instance') if 'km' in json.loads(x.proto.json_args))
assert reset_args['wind']['scale']==initial_scale
print('PASS one drag event updates only the working center; Reset persists across rerun without replaying stale component value',flush=True)

# Relocate the entire square away from the plant, still within the synthetic raster.
states=a._tree.get_widget_states()
component=next(x for x in a.get('component_instance') if 'km' in json.loads(x.proto.json_args))
move=states.widgets.add();move.id=component.proto.id
move.json_value=json.dumps({'action':'move','event_id':'test_move_28_far','lat':41.14,'lon':28.16})
a._run(states);assert not a.exception,a.exception
far=next(json.loads(x.proto.json_args) for x in a.get('component_instance') if 'km' in json.loads(x.proto.json_args))
assert far['polygon']==args['polygon']
assert far['working_polygon']!=args['working_polygon']
assert min(p[0] for p in far['working_polygon'])>max(p[0] for p in args['polygon'])
assert min(far['wind']['longitudes'])>max(args['wind']['longitudes'])
assert min(far['wind']['latitudes'])>max(args['wind']['latitudes'])
assert np.isfinite(np.array(far['wind']['matrix'],dtype=float)).sum()>100
assert not np.isclose(np.nanmean(np.array(far['wind']['matrix'],dtype=float)),np.nanmean(np.array(args['wind']['matrix'],dtype=float)))
assert far['wind']['scale']==initial_scale
for current in [args,moved_args,reset_args,far]:
 corners=current['working_polygon'];wind=current['wind']
 # Point-in-polygon excludes some boundary nodes; centers remain within one grid step.
 for axis,index in [('longitudes',0),('latitudes',1)]:
  lo=min(p[index] for p in corners);hi=max(p[index] for p in corners)
  step=(hi-lo)/59
  assert lo-1e-8<=min(wind[axis])<=lo+step+1e-8
  assert hi-step-1e-8<=max(wind[axis])<=hi+1e-8
print('PASS square completely outside plant receives a newly computed geographic field; sampled nodes cover orange geometry within one grid step, boundary and scale unchanged',flush=True)
