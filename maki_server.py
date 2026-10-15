"""Standard Streamlit cloud entry; Windows background upload service is disabled."""
from pathlib import Path
import runpy

runpy.run_path(
    str(Path(__file__).with_name('appv11.11.26_KARARLILIK_VE_TEMIZ_EKRAN.py')),
    run_name='__main__',
)
