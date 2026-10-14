"""Exercise actual PDF text extraction, previews, and raster-only OCR fallback."""
import ast, datetime, re
from pathlib import Path
import fitz
import pytesseract

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/'appv11.11.18_PDF_OKUMA_DESTEGI.py'
ns = {'re': re, 'datetime': datetime, 'Path': Path}
names = {'vaziyet_plani_pdf_ozeti', '_ondalik_sayi', '_dms_to_decimal',
         '_pdf_sayfa_ocr', '_pdf_tablo_metinleri', 'kurulum_raporu_pdf_oku'}
for node in ast.parse(source.read_text()).body:
    if isinstance(node, ast.FunctionDef) and node.name in names:
        node.decorator_list = []
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), ns)
text = '''The working title of the station is "Sample Mast".
Commissioning Date: 14.10.2026
Coordinates of the met mast
Geographic decimal WGS84 28.123456 40.654321
This is a synthetic installation report for dependency validation.
'''
doc = fitz.open()
page = doc.new_page(width=800, height=1000)
page.insert_textbox(fitz.Rect(40,40,760,950), text, fontsize=20)
data = doc.tobytes()
result = ns['kurulum_raporu_pdf_oku'](data)
assert result['hata'] is None, result['hata']
assert result['mast_name'] == 'Sample Mast', result['mast_name']
assert abs(result['latitude']-40.654321)<1e-8
assert abs(result['longitude']-28.123456)<1e-8
assert result['installation_date'] == '14.10.2026'
assert result['onizleme_png'].startswith(b'\x89PNG')
print('PASS text PDF: mast name, coordinates, date and PNG preview')
summary = ns['vaziyet_plani_pdf_ozeti'](data)
assert summary['hata'] is None
assert 'Sample Mast' in summary['metin']
assert summary['onizleme_png'].startswith(b'\x89PNG')
print('PASS site-plan PDF summary and preview')
image = page.get_pixmap(matrix=fitz.Matrix(2,2), alpha=False).tobytes('png')
scan = fitz.open()
p = scan.new_page(width=800,height=1000)
p.insert_image(p.rect, stream=image)
assert not p.get_text().strip(), 'OCR fixture must not contain a text layer'
assert {'tur','eng'}.issubset(pytesseract.get_languages())
ocr = ns['kurulum_raporu_pdf_oku'](scan.tobytes())
assert ocr['hata'] is None, ocr['hata']
assert 'Sample Mast' in ocr['metin'], ocr['metin']
assert ocr['onizleme_png'].startswith(b'\x89PNG')
print('PASS raster-only PDF: real Tesseract OCR with English/Turkish models, text and preview')
bad = ns['kurulum_raporu_pdf_oku'](b'not a PDF')
assert bad['hata']
print('PASS invalid PDF remains a reported read error')
old = ast.parse((ROOT/'previous_versions/appv11.11.17_BULUT_KLASOR_ERISIMI.py').read_text())
new = ast.parse(source.read_text())
funcs = lambda t: {n.name:ast.dump(n) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert funcs(old)==funcs(new)
print('PASS all application functions/classes unchanged; PyMuPDF',fitz.VersionBind)
