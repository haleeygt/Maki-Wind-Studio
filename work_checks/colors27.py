"""Moving the study window must not renormalize a fixed site's wind colors."""
from pathlib import Path
import ast,math
import numpy as np,pandas as pd
from pandas.testing import assert_frame_equal
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];NEW=ROOT/'appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py';OLD=ROOT/'previous_versions/appv11.11.26_KARARLILIK_VE_TEMIZ_EKRAN.py'
def extract(path):
 ns={'np':np,'pd':pd,'math':math}
 for n in ast.parse(path.read_text()).body:
  if isinstance(n,ast.FunctionDef) and n.name in {'surukle_ruzgar_overlay_uret','saha_ruzgar_renk_olcegi','nokta_poligon_icinde'}:
   exec(compile(ast.Module(body=[n],type_ignores=[]),str(path),'exec'),ns)
 return ns
old,new=extract(OLD),extract(NEW)
polygon=[[28,41],[28.03,41],[28.03,41.03],[28,41.03],[28,41]]
site=pd.DataFrame([{'lat':lat,'lon':lon,'Hub Rüzgar Hızı (m/s)':v,'Nokta Türü':'Raster grid'} for lat,lon,v in [(41.01,28.01,6),(41.01,28.02,6.5),(41.02,28.01,7),(41.02,28.02,7.5)]])
reference=site.copy(deep=True);reference.loc[len(reference)]=[42,29,30,'Raster grid'];reference.loc[len(reference)]=[41.015,28.015,40,'Direk kontrol noktası']
scale=new['saha_ruzgar_renk_olcegi'](reference,polygon)
assert scale['data_min']==6 and scale['data_max']==7.5
windows=[]
for outlier in [9,40]:
 outside=pd.DataFrame([{'lat':40.99,'lon':27.99,'Hub Rüzgar Hızı (m/s)':outlier,'Nokta Türü':'Raster grid'}])
 windows.append(pd.concat([site,outside],ignore_index=True))
old_a,old_b=[old['surukle_ruzgar_overlay_uret'](g,bosluklari_koru=True) for g in windows]
assert old_a['vmax']!=old_b['vmax']
print('PASS old scale reproduces outside-window values changing colors of the same plant values',flush=True)
overlays=[]
for window in windows:
 original=window.copy(deep=True)
 overlay=new['surukle_ruzgar_overlay_uret'](window,bosluklari_koru=True,renk_olcegi=scale)
 assert_frame_equal(window,original)
 assert overlay['vmin']==scale['vmin'] and overlay['vmax']==scale['vmax']
 assert overlay['matrix'][overlay['latitudes'].index(41.01)][overlay['longitudes'].index(28.02)]==6.5
 overlays.append(overlay)
assert new['saha_ruzgar_renk_olcegi'](site.assign(**{'Hub Rüzgar Hızı (m/s)':np.nan}),polygon) is None
flat=site.assign(**{'Hub Rüzgar Hızı (m/s)':6.5});flat_scale=new['saha_ruzgar_renk_olcegi'](flat,polygon)
assert flat_scale['uniform'] and flat_scale['vmin']<6.5<flat_scale['vmax']
assert flat_scale['vmax']-flat_scale['vmin']>=.5
near=site.assign(**{'Hub Rüzgar Hızı (m/s)':[6.5,6.501,6.502,6.503]})
near_scale=new['saha_ruzgar_renk_olcegi'](near,polygon);assert near_scale['vmax']-near_scale['vmin']>=.5
print('PASS fixed site scale ignores external outliers/control points, leaves measured values untouched and avoids exaggerating uniform/tiny variation',flush=True)
node=next(n for n in ast.parse(NEW.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='suruklenebilir_calisma_karesi')
html=next(n.value.value for n in ast.walk(node) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='html' for t in n.targets))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':540,'height':650});page.route('https://mt1.google.com/**',lambda route:route.abort());page.set_content(html)
 colors=[]
 for overlay,center in zip(overlays,[[41.04,28.04],[41.015,28.015]]):
  page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",{'polygon':polygon,'center':center,'working_polygon':[[27.95,40.95],[28.1,40.95],[28.1,41.1],[27.95,41.1],[27.95,40.95]],'km':10,'wind':overlay,'height':570})
  page.wait_for_function('center=>initialized && args.center[0]===center[0] && args.center[1]===center[1] && document.querySelector("#wind-layer")!==null',arg=center)
  colors.append(page.locator('#wind-layer rect[data-value="6.5"]').get_attribute('fill'))
  assert 'Sabit saha ölçeği' in page.locator('#range').inner_text()
 assert colors[0]==colors[1],colors
 raw_flat=new['surukle_ruzgar_overlay_uret'](flat,bosluklari_koru=True)
 page.evaluate("a=>window.postMessage({type:'streamlit:render',args:a},'*')",{'polygon':polygon,'center':[41.015,28.015],'working_polygon':[[27.95,40.95],[28.1,40.95],[28.1,41.1],[27.95,41.1],[27.95,40.95]],'km':10,'wind':raw_flat,'height':570})
 page.wait_for_function('args.wind.vmin===6.5 && args.wind.vmax===6.5')
 assert page.locator('#wind-layer rect[data-value="6.5"]').first.get_attribute('fill')!='rgb(23,59,255)'
 print('PASS actual browser renders identical colors for same values after moving center; constant field no longer maps automatically to minimum blue',flush=True)
 browser.close()
