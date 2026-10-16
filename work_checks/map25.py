"""Map registration across responsive widths and pan/zoom; missing cells stay missing."""
import ast,json,math,re
from pathlib import Path
import numpy as np,pandas as pd
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py';tree=ast.parse(SOURCE.read_text())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='suruklenebilir_calisma_karesi')
html=next(n.value.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='html' for t in n.targets))
helper=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='surukle_ruzgar_overlay_uret')
ns={'pd':pd,'np':np,'math':math}
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in {'latlon_xy_donustur','kare_calisma_alani_uret'}:exec(compile(ast.Module(body=[n],type_ignores=[]),str(SOURCE),'exec'),ns)
exec(compile(ast.Module(body=[helper],type_ignores=[]),str(SOURCE),'exec'),ns)
polygon=[[28.0,41.0],[28.025,41.0],[28.025,41.025],[28.0,41.025],[28.0,41.0]]
grid=pd.DataFrame([{'lat':lat,'lon':lon,'Hub Rüzgar Hızı (m/s)':None if (y,x)==(1,1) else 5+y+x/10} for y,lat in enumerate([41.003,41.012,41.021]) for x,lon in enumerate([28.003,28.012,28.021])])
original=grid.copy(deep=True);overlay=ns['surukle_ruzgar_overlay_uret'](grid,bosluklari_koru=True)
assert overlay['matrix'][1][1] is None
pd.testing.assert_frame_equal(grid,original)
assert overlay['vmin']==5 and overlay['vmax']==7.2
with_check=pd.concat([grid.assign(**{'Nokta Türü':'Raster grid'}),pd.DataFrame([{'lat':41.015,'lon':28.015,'Hub Rüzgar Hızı (m/s)':999,'Nokta Türü':'Direk kontrol noktası'}])],ignore_index=True)
assert ns['surukle_ruzgar_overlay_uret'](with_check,bosluklari_koru=True)==overlay
assert ns['surukle_ruzgar_overlay_uret'](grid.assign(**{'Hub Rüzgar Hızı (m/s)':np.nan}),bosluklari_koru=True) is None
print('PASS overlay preserves exact available grid values, missing cells and input frame; no invented wind field',flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in [390,960,1400]:
  page=browser.new_page(viewport={'width':width,'height':700})
  page.route('https://mt1.google.com/**',lambda route:route.abort())
  page.set_content(html)
  page.evaluate("window.messages=[];window.addEventListener('message',e=>{if(e.data.type==='streamlit:setComponentValue')messages.push(e.data.value)})")
  args={'polygon':polygon,'center':[41.0125,28.0125],'working_polygon':ns['kare_calisma_alani_uret'](polygon,10,[41.0125,28.0125]),'km':10,'height':570,'wind':overlay}
  page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",args)
  page.wait_for_function('initialized && document.querySelectorAll("#wind-layer rect").length===8')
  def registration():
   result=page.evaluate('''()=>{
    const p=args.polygon[0],world=merc(p[1],p[0]),tx=Math.floor(world[0]/256),ty=Math.floor(world[1]/256);
    const tile=document.querySelector(`#tiles img[data-tx="${tx}"][data-ty="${ty}"]`);
    if(!tile)throw new Error('Reference tile outside view');
    const v=document.getElementById('boundary').points.getItem(0),m=svg.getScreenCTM(),r=svg.getBoundingClientRect();
    const vector=new DOMPoint(v.x,v.y).matrixTransform(m);
    return {delta:[vector.x-r.left-(parseFloat(tile.style.left)+world[0]-tx*256),vector.y-r.top-(parseFloat(tile.style.top)+world[1]-ty*256)],polygon:args.polygon,center:args.center.slice()};
   }''')
   assert max(map(abs,result['delta']))<.05,result
   assert result['polygon']==polygon
   return result
  registration()
  old=page.evaluate('screen(41.0,28.0)')
  page.mouse.move(width*.2,220);page.mouse.down();page.mouse.move(width*.2+37,260,steps=4);page.mouse.up()
  new=page.evaluate('screen(41.0,28.0)');assert abs(new[0]-old[0]-37)<.05 and abs(new[1]-old[1]-40)<.05
  registration();assert page.evaluate('messages.length')==0
  page.mouse.move(width*.35,200);page.mouse.wheel(0,-100);page.wait_for_timeout(100);registration()
  assert page.evaluate('args.center')==args['center'] and page.evaluate('messages.length')==0
  page.set_viewport_size({'width':width+80,'height':700});page.wait_for_timeout(100);registration()
  assert page.locator('#study-clip polygon').get_attribute('points')!=page.locator('#boundary').get_attribute('points')
  assert page.evaluate('''()=>{const clip=document.querySelector('#study-clip polygon').getBBox(),square=document.getElementById('square').getBBox();return ['x','y','width','height'].every(k=>Math.abs(clip[k]-square[k])<.001)}''')
  assert page.evaluate('args.working_polygon')==[list(p) for p in args['working_polygon']]
  assert page.evaluate('''()=>{const layer=document.getElementById('wind-layer').getBBox(),square=document.getElementById('square').getBBox();return ['x','y','width','height'].every(k=>Math.abs(layer[k]-square[k])<.001)}''')
  print('PASS satellite/boundary/wind registration at width',width,'after pan, zoom and resize; pan leaves geographic boundary and working center unchanged',flush=True)
  if width==390:page.screenshot(path='/tmp/maki_map25_wind.png')
  c=page.locator('#square-handle').bounding_box();page.mouse.move(c['x']+c['width']/2,c['y']+c['height']/2);page.mouse.down();page.mouse.move(c['x']+c['width']/2+30,c['y']+c['height']/2+20,steps=4);page.mouse.up()
  page.wait_for_function('messages.length===1')
  assert page.evaluate('messages[0].action')=='move'
  assert page.evaluate('args.polygon')==polygon
  assert page.locator('#wind-layer').count()==0 # old grid cannot masquerade as recomputed data
  print('PASS explicit square-handle drag changes only working area and clears stale wind layer',width,flush=True)
  if width==390:page.screenshot(path='/tmp/maki_map25_narrow.png')
  page.close()
 browser.close()
# The turbine editor uses the same responsive tile/vector registration fix.
turbine=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='suruklenebilir_turbin_haritasi')
turbine_html=next(n.value.value for n in ast.walk(turbine) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='html_code' for t in n.targets))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':420,'height':700});page.route('https://mt1.google.com/**',lambda route:route.abort());page.set_content(turbine_html)
 args={'polygon':polygon,'points':[{'lat':41.012,'lon':28.012,'ad':'T1'}],'add_mode':False,'view_bounds':[[40.99,27.99],[41.035,28.04]],'wind':None}
 page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",args);page.wait_for_function('viewInitialized')
 def check_turbine():
  error=page.evaluate('''()=>{const p=args.polygon[0],w=worldXY(p[1],p[0],z),tx=Math.floor(w.x/256),ty=Math.floor(w.y/256),tile=document.querySelector(`#tiles img[data-tx="${tx}"][data-ty="${ty}"]`);if(!tile)throw new Error('Missing reference tile');const q=document.querySelector('.boundary').points.getItem(0),v=new DOMPoint(q.x,q.y).matrixTransform(svg.getScreenCTM()),r=svg.getBoundingClientRect();return [v.x-r.left-(parseFloat(tile.style.left)+w.x-tx*256),v.y-r.top-(parseFloat(tile.style.top)+w.y-ty*256)]}''')
  assert max(map(abs,error))<.05,error
 check_turbine();page.mouse.move(50,210);page.mouse.down();page.mouse.move(80,240,steps=4);page.mouse.up();check_turbine()
 page.mouse.move(210,260);page.mouse.wheel(0,-100);page.wait_for_timeout(100);check_turbine()
 page.set_viewport_size({'width':900,'height':700});page.wait_for_timeout(100);check_turbine()
 assert page.evaluate('args.polygon')==polygon
 assert page.evaluate('args.points[0].lat')==41.012 and page.evaluate('args.points[0].lon')==28.012
 print('PASS turbine map tile/boundary registration after pan, zoom and responsive resize; turbine coordinates unchanged',flush=True)
 browser.close()
# Verify the declared TIFF dependency can read a known north-up raster. This is
# a synthetic sampling check, not independent validation of actual GWA rasters.
import io,tifffile
sample=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_geotiff_ornekle')
ns={'np':np};exec(compile(ast.Module(body=[sample],type_ignores=[]),str(SOURCE),'exec'),ns)
raw=io.BytesIO();values=np.array([[5,6,7],[8,9,10]],dtype=np.float32)
tifffile.imwrite(raw,values,extratags=[(33550,'d',3,(.01,.01,0),False),(33922,'d',6,(0,0,0,28,41.02,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)])
actual,crs,bounds=ns['_gwa_geotiff_ornekle'](raw.getvalue(),np.array([28.005,28.025]),np.array([41.015,41.005]))
np.testing.assert_array_equal(actual,[5,10]);assert crs=='EPSG:4326'
print('PASS installed TIFF reader samples known georeferenced pixel centers correctly',flush=True)
