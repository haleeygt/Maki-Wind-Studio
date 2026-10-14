"""Check all prior cloud entry filenames and the main-screen folder connection."""
import ast
import tempfile
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
old = ast.parse((ROOT/'previous_versions/appv11.11.16_OTOMATIK_KLASOR_BAGLANTISI.py').read_text())
new = ast.parse((ROOT/'previous_versions/appv11.11.17_BULUT_KLASOR_ERISIMI.py').read_text())
functions = lambda tree: {n.name: ast.dump(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
assert all(functions(new)[k] == v for k, v in functions(old).items())
print('PASS all prior functions/classes unchanged')
for path in sorted([ROOT/'previous_versions/appv11.11.17_BULUT_KLASOR_ERISIMI.py']):
    app = AppTest.from_file(str(path), default_timeout=60).run()
    assert not app.exception, (path.name, app.exception)
    assert any(x.value == 'v11.11.17' for x in app.metric), path.name
    app.sidebar.button(key='v8_nav_Rüzgar Ölçümleri').click().run()
    assert not app.exception, (path.name, app.exception)
    assert any('Klasör izni bekleniyor' in x.value for x in app.info), path.name
    assert not any('LoggerNet klasörü bulunamadı:' in x.value for x in app.error)
    assert not any(x.key == 'loggernet_klasor_widget_v83' for x in app.text_input)
    print('PASS', path.name, 'opens current cloud folder-permission screen')
# An actually accessible local directory still uses the original local workflow.
with tempfile.TemporaryDirectory(prefix='maki_local_folder_') as folder:
    app.session_state['app_state']['loggernet_folder'] = folder
    app.run()
    assert not app.exception, app.exception
    assert any(x.key == 'loggernet_klasor_widget_v83' for x in app.text_input)
    assert any('WindData.dat' in x.value for x in app.warning)
print('PASS accessible local directory retains original local-file workflow')
