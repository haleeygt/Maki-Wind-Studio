# Compatibility entry point for existing Streamlit Cloud deployments.
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("appv11.11.17_BULUT_KLASOR_ERISIMI.py")), run_name="__main__")
