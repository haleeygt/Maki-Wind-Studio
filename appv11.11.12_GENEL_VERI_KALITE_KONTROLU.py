# Compatibility entry point for existing Streamlit Cloud deployments.
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("appv11.11.18_PDF_OKUMA_DESTEGI.py")), run_name="__main__")
