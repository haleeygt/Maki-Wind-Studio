"""A 1 GiB raster must sample through a few small tiles, never a full array."""
import ast,json,os,resource,subprocess,sys,tempfile
from pathlib import Path
import numpy as np,tifffile
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'appv11.11.28_CALISMA_KARESINDE_RUZGAR_HARITASI.py'
def sampler():
 tree=ast.parse(SOURCE.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_gwa_geotiff_ornekle')
 ns={'np':np};exec(compile(ast.Module(body=[node],type_ignores=[]),str(SOURCE),'exec'),ns)
 return ns['_gwa_geotiff_ornekle']
if '--sample' in sys.argv:
 fn=sampler();path=Path(sys.argv[2])
 original=tifffile.TiffPage.asarray;tifffile.TiffPage.asarray=lambda *a,**k:(_ for _ in ()).throw(AssertionError('full page allocation'))
 try:
  values,crs,bounds=fn(path,np.array([28.00005,28.81925,29.63835]),np.array([41.99995,41.18075,40.36165]))
 finally:tifffile.TiffPage.asarray=original
 np.testing.assert_array_equal(values,[6,6,6])
 print(json.dumps({'peak_mb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'values':values.tolist()}));raise SystemExit(0)
with tempfile.TemporaryDirectory(prefix='maki_raster26_') as tmp:
 path=Path(tmp)/'large.tif';block=np.full((256,256),6,dtype=np.float32)
 tags=[(33550,'d',3,(.0001,.0001,0),False),(33922,'d',6,(0,0,0,28,42,0),False),(34735,'H',8,(1,1,0,1,2048,0,1,4326),False)]
 tifffile.imwrite(path,data=(block for _ in range(64*64)),shape=(16384,16384),dtype=np.float32,tile=(256,256),compression='deflate',maxworkers=1,extratags=tags)
 completed=subprocess.run([sys.executable,__file__,'--sample',str(path)],capture_output=True,text=True,check=True)
 result=json.loads(completed.stdout);assert result['peak_mb']<256,result
 print('PASS 1 GiB raster sampled correctly; isolated-process peak',round(result['peak_mb'],1),'MiB; full-page allocation prohibited',flush=True)
 # A single huge strip must be rejected BEFORE decompression.
 large=Path(tmp)/'oversized-strip.tif'
 tifffile.imwrite(large,np.full((4096,4096),6,dtype=np.float32),rowsperstrip=4096,compression='deflate',extratags=tags,maxworkers=1)
 try:
  sampler()(large,np.array([28.00005]),np.array([41.99995]));raise AssertionError('unsafe strip accepted')
 except RuntimeError as error:assert 'bellek sınır' in str(error)
 print('PASS oversized TIFF strip rejected before allocation; existing measurements untouched',flush=True)
