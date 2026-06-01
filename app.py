import streamlit as st

from OTM_Table_Generator import main as render_generator
from pages.Documentation import render as render_documentation

st.set_page_config(page_title='OTM Table Generator', page_icon='🤖', layout='wide')

tab1, tab2 = st.tabs(['⚙️ OTM Table Generator', '📜 Documentation'])

with tab1:
    render_generator()

with tab2:
    render_documentation()
