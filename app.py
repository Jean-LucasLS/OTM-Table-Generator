import streamlit as st

st.set_page_config(page_title='OTM Table Generator', page_icon='🤖', layout='wide')

pg = st.navigation([
    st.Page('OTM_Table_Generator.py', title='OTM Table Generator', icon='⚙️'),
    st.Page('pages/Documentation.py',  title='Documentation',        icon='📜'),
])
pg.run()
