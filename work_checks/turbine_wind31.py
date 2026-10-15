"""Regression for tall wind stripes in the manual turbine editor."""
import ast,math
from pathlib import Path
import numpy as np,pandas as pd
from pandas.testing import assert_frame_equal
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];NEW=ROOT/'appv11.11.31_TURBIN_RUZGAR_KATMANI_DUZELTMESI.py';OLD=ROOT/'previous_versions/appv11.11.30_YENIDEN_CALISMA_BELLEK_KORUMASI.py'
def extract(path):
 tree=ast.parse(path.read_text());ns={'pd':pd,'np':np,'math':math}
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='surukle_ruzgar_overlay_uret');exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),ns)
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='suruklenebilir_turbin_haritasi')
 html=next(n.value.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='html_code' for t in n.targets))
 return ns['surukle_ruzgar_overlay_uret'],html
old,old_html=extract(OLD);new,html=extract(NEW)
grid=pd.DataFrame([{'lat':lat,'lon':lon,'Hub Rüzgar Hızı (m/s)':np.nan if (i,j)==(1,1) else 6+i*.1+j*.05,'Nokta Türü':'Raster grid'} for i,lat in enumerate([41.,41.01,41.02]) for j,lon in enumerate([28.,28.01,28.02])])
grid.loc[len(grid)]=[38.,28.0001,9.,'Direk kontrol noktası'];original=grid.copy(deep=True)
legacy=old(grid);assert abs(legacy['latitudes'][1]-legacy['latitudes'][0])==3
scale={'vmin':5.5,'vmax':7.5,'scope':'santral'}
wind=new(grid,bosluklari_koru=True,renk_olcegi=scale)
assert wind['latitudes']==[41.,41.01,41.02] and wind['longitudes']==[28.,28.01,28.02]
assert wind['matrix'][1][1] is None and wind['scale']==scale
assert new(grid)['latitudes']==[41.,41.01,41.02]
assert_frame_equal(grid,original)
print('PASS old manual path reproduces 3-degree tall cells; new overlay excludes control points, preserves actual grid and missing cells',flush=True)
polygon=[[27.995,40.995],[28.025,40.995],[28.025,41.025],[27.995,41.025],[27.995,40.995]]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in [390,960,1400]:
  page=browser.new_page(viewport={'width':width,'height':700});page.route('https://mt1.google.com/**',lambda route:route.abort());page.set_content(html)
  page.evaluate("window.updates=[];window.addEventListener('message',e=>{if(e.data.type==='streamlit:setComponentValue')updates.push(e.data.value)})")
  args={'polygon':polygon,'points':[{'lat':41.012,'lon':28.012,'ad':'T1'}],'add_mode':False,'view_bounds':[[40.99,27.99],[41.03,28.03]],'wind':wind}
  page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",args);page.wait_for_function('viewInitialized && document.querySelectorAll("#turbine-wind-layer rect").length===8')
  def check():
   delta=page.evaluate('''()=>{const r=document.getElementById('turbine-wind-layer').getBBox(),a=screenXY(41.025,27.995),b=screenXY(40.995,28.025);return [r.x-a.x,r.y-a.y,r.width-(b.x-a.x),r.height-(b.y-a.y)]}''')
   assert max(map(abs,delta))<.001,delta
  check();page.mouse.move(width*.15,100);page.mouse.down();page.mouse.move(width*.15+20,120,steps=3);page.mouse.up();check()
  page.mouse.move(width/2,280);page.mouse.wheel(0,-100);page.wait_for_timeout(100);check()
  # Pointer coordinates must use the same 1000x570 SVG viewBox as screenToLL.
  box=page.locator('.turb').bounding_box();cx=box['x']+box['width']/2;cy=box['y']+box['height']/2
  expected=page.evaluate('''([x,y])=>{const r=svg.getBoundingClientRect();return screenToLL((x-r.left)*1000/r.width,(y-r.top)*570/r.height)}''',[cx+4,cy+3])
  page.mouse.move(cx,cy);page.mouse.down();page.mouse.move(cx+4,cy+3,steps=3);page.mouse.up();page.wait_for_function('updates.length>0')
  point=page.evaluate('updates.at(-1).points[0]');assert abs(point['lat']-expected['lat'])<1e-8 and abs(point['lon']-expected['lon'])<1e-8,(point,expected)
  assert page.evaluate('args.polygon')==polygon
  page.set_viewport_size({'width':width+70,'height':700});page.wait_for_timeout(100);check()
  # Nonuniform axis spacing also uses each cell's neighbor midpoints.
  irregular=dict(wind);irregular['latitudes']=[41.,41.002,41.02];irregular['longitudes']=[28.,28.001,28.02]
  args['wind']=irregular;page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",args)
  page.wait_for_function('args.wind.latitudes[1]===41.002')
  extent=page.evaluate('''()=>{const r=document.getElementById('turbine-wind-layer').getBBox(),a=screenXY(41.029,27.9995),b=screenXY(40.999,28.0295);return [r.x-a.x,r.y-a.y,r.width-(b.x-a.x),r.height-(b.y-a.y)]}''')
  assert max(map(abs,extent))<.001,extent
  print('PASS browser width',width,'local wind extent/missing cell, pan/zoom/resize, correct turbine drag, irregular coordinate edges',flush=True)
  page.close()
 browser.close()
