"""Actual UI regression, disk-cache isolation and bounded TIFF sampling."""
from pathlib import Path
import ast,contextlib,hashlib,io,json,math,os,re,tempfile,uuid,zipfile,gzip
import numpy as np,pandas as pd,tifffile
from pandas.testing import assert_frame_equal
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT/'previous_versions/appv11.11.25_SABIT_SINIR_RUZGAR_HARITASI.py';NEW=ROOT/'appv11.11.29_COKLU_DOSYA_BELLEK_KONTROLU.py'
BANNER='LoggerNet TOA5 veya standart CSV WindData dosyasını güvenli biçimde okur.'
names={'_loggernet_okuma_kilidi','_loggernet_cache_dizini','_loggernet_oku_dogrudan','loggernet_oku'}
for source,leaks in [(OLD,True),(NEW,False)]:
 text=source.read_text();tree=ast.parse(text)
 code='import streamlit as st\nimport numpy as np,pandas as pd,re\nRUZGAR_KOLONLARI=["WS1_Avg","WS2_Avg","WS3_Avg","WS4_Avg"]\n'
 for node in tree.body:
  if isinstance(node,ast.FunctionDef) and node.name in names:
   start=min([node.lineno]+[d.lineno for d in node.decorator_list])-1
   code+=''.join(text.splitlines(True)[start:node.end_lineno])+'\n\n'
 code+="_result=loggernet_oku(b'TIMESTAMP,WS1_Avg\\n2025-01-01 00:00:00,6\\n')\n"
 app=AppTest.from_string(code,default_timeout=30).run();assert not app.exception,app.exception
 assert any(BANNER in x.value for x in app.markdown)==leaks
 app.run();assert not app.exception,app.exception
 assert any(BANNER in x.value for x in app.markdown)==leaks
print('PASS old reader reproduces unwanted UI output; new reader emits none on first read and repeated read',flush=True)
text=NEW.read_text();tree=ast.parse(text)
with tempfile.TemporaryDirectory(prefix='maki_stability26_') as tmp:
 ns={'__file__':str(Path(tmp)/'app.py'),'Path':Path,'np':np,'pd':pd,'re':re,'os':os,'uuid':uuid,'zipfile':zipfile,'gzip':gzip,'io':io,'json':json,'hashlib':hashlib,'RUZGAR_KOLONLARI':['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg']}
 wanted=names|{'_gwa_geotiff_ornekle','_gwa_cache_dir','_gwa_raster_dosyasini_ayikla','_gwa_http_raster_getir','_gwa_json_url_adaylari'}
 for node in tree.body:
  if isinstance(node,ast.FunctionDef) and node.name in wanted:
   node.decorator_list=[];exec(compile(ast.Module(body=[node],type_ignores=[]),str(NEW),'exec'),ns)
 raw=b'TIMESTAMP,WS1_Avg\n2025-01-01 00:00:00,6\n'
 first=ns['loggernet_oku'](raw);first.loc[0,'WS1_Avg']=99
 second=ns['loggernet_oku'](raw);assert float(second.WS1_Avg.iloc[0])==6
 path=next(ns['_loggernet_cache_dizini']().glob('*.pkl'));path.write_bytes(b'corrupted')
 third=ns['loggernet_oku'](raw);assert float(third.WS1_Avg.iloc[0])==6
 assert not list(ns['_loggernet_cache_dizini']().glob('*.tmp'))
 print('PASS disk cache returns independent measurements, repairs corrupted cache and commits atomically',flush=True)
 # Equivalent pixels for both stripped and tiled, raw and lossless-deflate rasters.
 tags=[(33550,'d',3,(.01,.01,0),False),(33922,'d',6,(0,0,0,28,42,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)]
 values=np.linspace(4,12,64*80,dtype=np.float32).reshape(64,80)
 rows=np.array([0,7,16,31,32,63,14]);cols=np.array([0,79,17,30,45,79,20])
 lons=28+(cols+.5)*.01;lats=42-(rows+.5)*.01
 for tiled in [False,True]:
  for compression in [None,'deflate']:
   out=io.BytesIO();kwargs={'tile':(16,16)} if tiled else {'rowsperstrip':8}
   tifffile.imwrite(out,values,compression=compression,extratags=tags,**kwargs)
   sample=Path(tmp)/f'{tiled}_{compression}.tif';sample.write_bytes(out.getvalue())
   # Fail the test if production tries to materialize the whole page.
   original=tifffile.TiffPage.asarray
   tifffile.TiffPage.asarray=lambda *a,**k:(_ for _ in ()).throw(AssertionError('whole raster allocation'))
   try:
    actual,crs,bounds=ns['_gwa_geotiff_ornekle'](sample,lons,lats)
    np.testing.assert_array_equal(actual,values[rows,cols])
   finally:tifffile.TiffPage.asarray=original
 print('PASS tiled/stripped and deflate/raw pixel sampling exact with whole-page allocation prohibited',flush=True)
 # One 64x80 file has 40 tiles; only tiles touching the seven query points decode.
 count=[];original_decode=tifffile.TiffPage.decode
 # Cached-property decode cannot be patched as a normal bound method; intercept reads instead.
 original_read=tifffile.FileHandle.read
 def tracked_read(self,size=-1):
  if size>=16*16*4:count.append(size)
  return original_read(self,size)
 tifffile.FileHandle.read=tracked_read
 try:ns['_gwa_geotiff_ornekle'](Path(tmp)/'True_None.tif',lons,lats)
 finally:tifffile.FileHandle.read=original_read
 assert len(count)<=len(rows)+2,len(count)
 print('PASS sparse sampling reads only required raster segments',flush=True)
 # Streaming extraction supports compressed API responses without ZIP/GZIP RAM expansion.
 for suffix,payload in [('zip',None),('gz',None)]:
  target=Path(tmp)/('test.'+suffix)
  if suffix=='zip':
   with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:archive.write(Path(tmp)/'True_None.tif','country.tif')
  else:
   with gzip.open(target,'wb') as output:output.write((Path(tmp)/'True_None.tif').read_bytes())
  extracted=ns['_gwa_raster_dosyasini_ayikla'](target)
  assert extracted.read_bytes()==(Path(tmp)/'True_None.tif').read_bytes()
 print('PASS ZIP/GZIP raster extraction preserves exact bytes on disk',flush=True)
 # Network response mocks enforce bounded reads and preserve TLS defaults in production.
 import urllib.request,urllib.parse
 ns['urllib']=__import__('urllib')
 class Response:
  def __init__(self,data,url,declared=None):self.data=data;self.offset=0;self.url=url;self.headers={'Content-Length':str(len(data) if declared is None else declared)};self.sizes=[]
  def read(self,size=-1):
   assert 0<size<=1024*1024,'unbounded network read'
   self.sizes.append(size);result=self.data[self.offset:self.offset+size];self.offset+=len(result);return result
  def __enter__(self):return self
  def __exit__(self,*args):return False
 original_open=urllib.request.urlopen;responses=[]
 def open_fake(req,timeout):
  data=json.dumps({'url':'https://example.invalid/country.tif'}).encode() if req.full_url.endswith('/api') else (Path(tmp)/'True_None.tif').read_bytes()
  response=Response(data,req.full_url);responses.append(response);return response
 urllib.request.urlopen=open_fake
 try:
  downloaded,url=ns['_gwa_http_raster_getir']('https://example.invalid/api')
  assert downloaded.read_bytes()==(Path(tmp)/'True_None.tif').read_bytes()
  assert len(responses)==2 and all(response.sizes for response in responses)
  urllib.request.urlopen=lambda req,timeout:Response(b'',req.full_url,600*1024*1024)
  try:ns['_gwa_http_raster_getir']('https://example.invalid/too-large.tif');raise AssertionError('oversized response accepted')
  except RuntimeError as error:assert 'sınır' in str(error)
 finally:urllib.request.urlopen=original_open
 assert not list(ns['_gwa_cache_dir']().glob('.download-*.tmp'))
 print('PASS API URL-following uses bounded reads; oversized downloads rejected and staging cleaned',flush=True)
