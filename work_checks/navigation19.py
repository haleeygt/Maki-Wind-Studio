from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
root=Path(__file__).resolve().parents[1]
a=AppTest.from_file(str(root/'appv11.11.12_GENEL_VERI_KALITE_KONTROLU.py'),default_timeout=60).run()
assert not a.exception,a.exception
x=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=144,freq='10min')})
for k,v in zip(['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg'],[6,5.8,5.5,5]):x[k]=v
x['WD1_Avg']=200;x['WD2_Avg']=210
state=a.session_state['app_state']
state['wind_data_files']=[{'name':'Generic_Mast.csv','bytes':x.to_csv(index=False).encode()}]
state['data_source']='Manuel dosya yükleme'
state['sensor_heights']={'Generic_Mast.csv':dict(zip(['WS1_Avg','WS2_Avg','WS3_Avg','WS4_Avg'],[83.,78.5,60.,40.]))}
assert not state['quality_approvals']
a.sidebar.button(key='v8_nav_Üretim Hesaplama').click().run()
assert not a.exception,a.exception
assert a.session_state['app_state']['active_page']=='Üretim Hesaplama'
assert not any(b.key=='energy_review_required' for b in a.button)
assert any('Halihazır Harita' in h.value for h in a.markdown)
assert not a.session_state['app_state']['quality_approvals']
print('PASS direct sidebar navigation before quality review; no gate and no synthetic approval')
a.sidebar.button(key='v8_nav_Rüzgar Kaynağı Özeti').click().run()
assert not a.exception,a.exception
assert a.button(key='energy_continue_v111119')
assert not a.button(key='energy_continue_v111119').disabled
assert not any(b.key=='approve_clean_energy_v111110' for b in a.button)
a.button(key='energy_continue_v111119').click().run()
assert not a.exception,a.exception
assert a.session_state['app_state']['active_page']=='Üretim Hesaplama'
print('PASS summary continues directly without approval checkbox or approval record')
# Invalid cadence does not block opening the map page; calculation checks are tested separately.
x.loc[1,'TIMESTAMP']=x.loc[0,'TIMESTAMP']
a.session_state['app_state']['wind_data_files']=[{'name':'Generic_Mast.csv','bytes':x.to_csv(index=False).encode()}]
a.sidebar.button(key='v8_nav_Ana Sayfa').click().run()
a.sidebar.button(key='v8_nav_Üretim Hesaplama').click().run()
assert not a.exception,a.exception
assert a.session_state['app_state']['active_page']=='Üretim Hesaplama'
assert not any(b.key=='energy_review_required' for b in a.button)
print('PASS map page accessible with invalid cadence; no quality-review navigation gate')
