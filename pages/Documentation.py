import numpy as np
import pandas as pd
import streamlit as st

from io import BytesIO
from otm_generator import rate_geo, rate_geo_cost_ton, rate_geo_cost_viagem
from OTM_Table_Generator import to_excel

model  = pd.DataFrame({'ORIGEM': ['FSCB', 'FAB_SUZ_1101'], 'DESTINO': ['L123456789', 'L123456789'], 'SAP': [123456, 123456], 'VEICULO': ['Y06', 'Y06'], 'FRETE': [44.44, 44.44]})
model2 = pd.DataFrame({'📍 ORIGEM': ['FAB_SUZ_1101', 'FAB_SUZ_1101']})
model3 = pd.DataFrame({'📍 ORIGEM': ['FSCB', 'FSCB', 'DSUZ', 'DSUZ'], '🎯 DESTINO': ['L111111111', 'L999999999', 'L111111111', 'L999999999'], '🏷️ SAP': ['444444', '444444', '888888', '888888'], '🚚 VEICULO': ['Y06', 'Y06', 'Y12', 'Y12'], '💸 FRETE': [22.22, 44.44, 88.88, 16.16]})
model4 = pd.DataFrame({'💾 ID_OTM': ['UN_0000444444_FAB_SUZ_1101_Y06', 'UN_0000888888_AMZ_SZL_1001_Y12']})
model5 = pd.DataFrame({'📍 ORIGEM': ['FSCB', 'ABDC', 'DSUZ', 'WXYZ']}).rename_axis('Index')

st.set_page_config(page_title='Documentation', page_icon='📜', layout='wide') # 🗂️

st.header(body='📜 Documentation 🗃️', divider='green');  st.text('')

col1, col2 = st.columns([4, 1])
with col1:
  st.subheader('📑 Utilização da tabela modelo (disponível para download 📥)')
with col2:
  model_excel = to_excel(model)
  if st.download_button(label='📥 model.xlsx', data=model_excel, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download da tabela modelo'):
    st.toast('Model table downloaded!')
st.markdown('📌 As colunas são :green-background[ORIGEM | DESTINO | SAP | VEICULO | FRETE], e :red-background[acusarão erro] caso não estejam neste formato')
st.dataframe(model, hide_index=True,
            column_config={
            'ORIGEM': st.column_config.TextColumn(label='📍 ORIGEM'),
            'DESTINO': st.column_config.TextColumn(label='🎯 DESTINO'),
            'SAP': st.column_config.TextColumn(label='🏷️ SAP'),
            'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO'),
            'FRETE': st.column_config.NumberColumn(label='💸 FRETE', format='%.2f R$')
            })

st.divider()

st.subheader('📑 Formatos aceitos para os campos de ORIGEM')
st.markdown('📌  Podem ser escritos no :green-background[formato do SAP ou OTM] e devem constar no dicionário. Exemplo: Tanto FSCB quanto FAB_SUZ_1101 irão resultar em FAB_SUZ_1101')
col1, col2, col3, col4 = st.columns([0.75, 0.25, 1, 3])
with col1:
  st.dataframe(model['ORIGEM'], hide_index=True, column_config={'ORIGEM': st.column_config.TextColumn(label='📍 ORIGEM')})
with col2:
  st.text('');  st.text('');  st.markdown('➡️➡️')
with col3:
  st.dataframe(model2, hide_index=True)
st.markdown('📌 :green-background[Origens incorretas] e/ou não listadas no dicionário :red-background[serão excluídas das tabelas geradas] para evitar cadastros incorretos, e :blue-background[evidenciadas em uma tabela a parte] mostrando os índices das linhas incorretas')
col1, col2, col3, col4 = st.columns([1.25, 0.25, 2, 4])
with col1:
  st.dataframe(model5)
with col2:
  st.text('');  st.text('');  st.text('');  st.text('')
  st.markdown('➡️➡️')
with col3:
  st.markdown('❗ Not-mapped origins')
  st.dataframe(model5.loc[[1, 3]], column_config={'📍 ORIGEM': st.column_config.TextColumn(label='⚠️ ORIGEM')})
st.markdown('📌 :green-background[Consultar o dicionário das origens] com o time de SupriLog e :blue-background[solicitar acréscimo] caso não haja registro de alguma em específico')

st.divider()

st.subheader("📑 Tratamento de duplicatas nos ID's")
st.markdown("📌 Rate Geo e Rate Geo Cost Group terão as :blue-background[duplicatas removidas] no :green-background[agrupamento ORIGEM + SAP + VEICULO], para :red-background[evitar o cadastro de dois ID's iguais]")
col1, col2, col3, col4, col5 = st.columns([1.25, 0.2, 1, 0.2, 1.25])
with col1:
  st.dataframe(model3, hide_index=True, column_config={'💸 FRETE': st.column_config.NumberColumn(format='%.2f R$')})
with col2:
  st.text('');  st.text('');  st.text('');  st.text('')
  st.markdown('➡️➡️')
with col3:
  st.dataframe(model3[['📍 ORIGEM', '🏷️ SAP', '🚚 VEICULO']], hide_index=True,  column_config={'SAP': st.column_config.TextColumn(label='🏷️ DESTINO'),
                                                                           'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO')})
with col4:
  st.text('');  st.text('');  st.text('');  st.text('')
  st.markdown('➡️➡️')
with col5:
  st.text('');  st.text('')
  st.dataframe(model4, hide_index=True)

st.divider()

st.subheader('📑 Especificidade das tabelas por Unidade de Negócio')
st.markdown('📌 As tabelas geradas contemplam a as :green-background[particularidades de cada Unidade de Negócio], sendo possível de :blue-background[selecionar a UN desejada]')
col1, col2 = st.columns([3, 7])
with col1:
  st.selectbox('Escolha a Unidade de Negócio:', ('UNPE', 'UNBC', 'UNC'))
st.markdown('📌 :blue-background[Procurar o responsável da UN] pelos cadastros no OTM :green-background[em caso de dúvidas]')