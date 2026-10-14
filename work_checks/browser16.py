"""Cloud folder ingestion checks; no credentials, no native Windows dialog required."""
import ast, base64, copy, datetime, hashlib, re, uuid
from pathlib import Path
import numpy as np
import pandas as pd
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'appv11.11.16_OTOMATIK_KLASOR_BAGLANTISI.py'
state = {'wind_data_files': [], 'production_result': {'old': True}}
ns = {'np': np, 'pd': pd, 're': re, 'hashlib': hashlib, 'base64': base64,
      'datetime': datetime, 'app_state': state, 'st': SimpleNamespace(session_state={}), 'LOGGERNET_PARCA_BOYUTU': 128,
      'RUZGAR_KOLONLARI': ['WS1_Avg', 'WS2_Avg', 'WS3_Avg', 'WS4_Avg']}
names = {'loggernet_oku', 'tarayici_loggernet_kaydini_hazirla',
         'tarayici_loggernet_kaydini_uygula', 'tarayici_loggernet_parcasini_al'}
for node in ast.parse(SOURCE.read_text()).body:
    if isinstance(node, ast.FunctionDef) and node.name in names:
        node.decorator_list = []
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), ns)

folder = str(uuid.uuid4())
def event(name='Mast_B_WindData.dat', value=6.0, folder_id=folder):
    content = pd.DataFrame({'TIMESTAMP': pd.date_range('2025-01-01', periods=8, freq='10min'),
                            'WS1_Avg': value, 'WS2_Avg': 5.8}).to_csv(index=False).encode()
    return {'action': 'file', 'event_id': str(uuid.uuid4()), 'folder_id': folder_id,
            'name': name, 'size': len(content), 'mtime_ms': 1735689600000,
            'sha256': hashlib.sha256(content).hexdigest(),
            'base64': base64.b64encode(content).decode()}

def rejected(evt):
    before = copy.deepcopy(state)
    try:
        ns['tarayici_loggernet_kaydini_uygula'](evt)
    except ValueError:
        assert state == before, 'Rejected event mutated prior data'
    else:
        raise AssertionError('Expected rejected transfer')

first = event()
ns['tarayici_loggernet_kaydini_uygula'](first)
assert state['wind_data_files'][0]['bytes'] == base64.b64decode(first['base64'])
assert state['production_result'] is None
ns['tarayici_loggernet_kaydini_uygula'](event('Mast_A_WindData.dat'))
ns['tarayici_loggernet_kaydini_uygula'](event(value=7.0))
assert [r['name'] for r in state['wind_data_files']] == ['Mast_B_WindData.dat', 'Mast_A_WindData.dat']
assert ns['loggernet_oku'](state['wind_data_files'][0]['bytes']).WS1_Avg.eq(7).all()
print('PASS byte-exact raw snapshot; changed file updates; mast order stays stable; stale energy cleared')

rejected({**event(), 'sha256': '0' * 64})
rejected({**event(), 'size': 1})
rejected({**event(), 'base64': 'not-base64'})
rejected(event('../Mast_WindData.dat'))
rejected(event('Ignore_RawData.dat'))
rejected(event('mast_b_winddata.dat'))
rejected(event(folder_id=str(uuid.uuid4())))
rejected({**event(), 'mtime_ms': float('nan')})
bad = event()
content = base64.b64decode(bad['base64']).rstrip(b'\n')
bad.update(size=len(content), base64=base64.b64encode(content).decode(), sha256=hashlib.sha256(content).hexdigest())
rejected(bad)
content = b'TIMESTAMP,WS1_Avg\nnot-a-date,6\n'
bad.update(size=len(content), base64=base64.b64encode(content).decode(), sha256=hashlib.sha256(content).hexdigest())
rejected(bad)
print('PASS corrupted/truncated/invalid-time payloads rejected atomically; unsafe names and mixed folders rejected')
state['wind_data_files'] = [{'name': 'existing.csv', 'source': 'manual', 'bytes': b'unchanged'}]
rejected(event())
print('PASS existing manual project not overwritten')

old = ast.parse((ROOT / 'appv11.11.15_SIYAH_BASLIK.py').read_text())
new = ast.parse(SOURCE.read_text())
functions = lambda tree: {n.name: ast.dump(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
assert all(functions(new).get(k) == v for k, v in functions(old).items())
print('PASS all prior parser/QC/reconstruction/energy/GIS functions and classes unchanged')

# Exercise multiple chunks with a small test bound; production chunks are 4 MiB.
state['wind_data_files'] = []
whole = event()
raw = base64.b64decode(whole['base64'])
chunks = [raw[i:i+128] for i in range(0, len(raw), 128)]
transfer = str(uuid.uuid4())
for index, data in enumerate(chunks):
    chunk = {**whole, 'action': 'chunk', 'transfer_id': transfer,
             'part_index': index, 'parts': len(chunks),
             'base64': base64.b64encode(data).decode()}
    done = ns['tarayici_loggernet_parcasini_al'](chunk)
    assert done == (index == len(chunks)-1)
    if not done: assert not state['wind_data_files'], 'Partial file became active'
assert state['wind_data_files'][0]['bytes'] == raw
assert '_browser_loggernet_transfer' not in ns['st'].session_state
prior = copy.deepcopy(state)
# Reordered and corrupt-final transfers must not replace the complete prior snapshot.
for index, data in enumerate(chunks):
    chunk = {**whole, 'action': 'chunk', 'sha256': '0'*64,
             'transfer_id': str(uuid.UUID(int=1)), 'part_index': index,
             'parts': len(chunks), 'base64': base64.b64encode(data).decode()}
    if index == len(chunks)-1:
        try: ns['tarayici_loggernet_parcasini_al'](chunk)
        except ValueError: pass
        else: raise AssertionError('Corrupt whole-file checksum accepted')
    else: ns['tarayici_loggernet_parcasini_al'](chunk)
assert state == prior
chunk['transfer_id'] = str(uuid.uuid4())
try: ns['tarayici_loggernet_parcasini_al'](chunk)
except ValueError: pass
else: raise AssertionError('Out-of-order chunk accepted')
assert state == prior
print('PASS chunk transport; partial data invisible; bad checksum and out-of-order chunks preserve prior data')
