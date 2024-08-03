import numpy as np
import pandas as pd
import streamlit as st

from io import BytesIO
from otm_generator import rate_geo, rate_geo_cost_ton, rate_geo_cost_viagem
from OTM_Table_Generator import to_excel

model = pd.DataFrame({'ORIGEM': ['FSCB', 'FAB_SUZ_1101'], 'DESTINO': ['L123456789', 'L123456789'], 'SAP': [123456, 123456], 'VEICULO': ['Y06', 'Y06'], 'FRETE': [44.44, 44.44]})

st.set_page_config(page_title='Documentation', page_icon='📜', layout='wide') # 🗂️

st.header(body='📜 Documentation 🗃️', divider='green')
st.text('')

col1, col2 = st.columns([4, 1])
with col1:
  st.markdown('1. O modelo de tabela deve conter as colunas do modelo (disponível para download 📥)')
with col2:
  model_excel = to_excel(model)
  if st.download_button(label='📥 model.xlsx', data=model_excel, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download da tabela modelo'):
    st.toast('Model table downloaded!')

st.dataframe(model, hide_index=True,
            column_config={
            'ORIGEM': st.column_config.TextColumn(label='📍 ORIGEM'),
            'DESTINO': st.column_config.TextColumn(label='🎯 DESTINO'),
            'SAP': st.column_config.TextColumn(label='🏷️ SAP'),
            'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO'),
            'FRETE': st.column_config.NumberColumn(label='💸 FRETE', format='%.2f R$')
            })

