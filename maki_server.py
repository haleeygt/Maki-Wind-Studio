"""Cloud entry point: Streamlit UI plus authenticated LoggerNet HTTPS ingestion."""
import os
import streamlit as st
from maki_ingest import upload_routes
os.environ['MAKI_SYNC_SERVICE'] = '1'
app = st.App('appv11.11.21_LOGGERNET_ARKAPLAN.py', routes=upload_routes)

if __name__ == '__main__':
    app.run()
