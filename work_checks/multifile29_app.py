"""Switch active measurements while all five datasets remain available."""
from pathlib import Path
import pandas as pd,numpy as np
from streamlit.testing.v1 import AppTest
root=Path(__file__).resolve().parents[1]
a=AppTest.from_file(str(root/'maki_server.py'),default_timeout=60).run();assert not a.exception
files=[];heights={}
for i in range(5):
 f=pd.DataFrame({'TIMESTAMP':pd.date_range('2025-01-01',periods=144,freq='10min')})
 for j in range(1,5):f[f'WS{j}_Avg']=4+i+j*.1+np.sin(np.arange(144)/10)*.2
 f['WD1_Avg']=210;name=f'Test_{i}.csv';files.append({'name':name,'bytes':f.to_csv(index=False).encode()})
 heights[name]={'WS1_Avg':85,'WS2_Avg':70,'WS3_Avg':60,'WS4_Avg':40}
state=a.session_state['app_state'];state['data_source']='Manuel dosya yükleme';state['wind_data_files']=files;state['sensor_heights']=heights
state['active_wind_data']='Direk 1 · Test_0.csv'
a.sidebar.button(key='v8_nav_Veri İnceleme').click().run();assert not a.exception,a.exception
selector=a.selectbox(key='tek_veri_secimi_v11119');assert len(selector.options)==5
first=a.dataframe[0].value.copy()
selector.select('Direk 5 · Test_4.csv').run();assert not a.exception,a.exception
assert a.session_state['app_state']['active_wind_data']=='Direk 5 · Test_4.csv'
last=a.dataframe[0].value
assert not first.equals(last)
a.selectbox(key='tek_veri_secimi_v11119').select('Direk 1 · Test_0.csv').run();assert not a.exception,a.exception
pd.testing.assert_frame_equal(a.dataframe[0].value,first)
print('PASS five datasets remain selectable; switching changes displayed data and returning restores identical table')
