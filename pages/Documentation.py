import streamlit as st

from ui.documentation_data import get_documentation_examples, get_origens_df
from ui.excel_utils import to_excel
from ui.styles import apply_basic_style
from ui.table_configs import doc_duplicate_table_column_config, doc_frete_column_config, model_table_column_config


def render():
  model, model2, model3, model4, model5 = get_documentation_examples()

  apply_basic_style()

  st.header(body='📜 Documentation', divider='green')
  st.text('')

  col1, col2 = st.columns([4, 1])
  with col1:
    st.subheader('Utilização da tabela modelo')
  with col2:
    model_excel = to_excel(model)
    if st.download_button(label='📥 model.xlsx', data=model_excel, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download da tabela modelo', key='model_download_documentation'):
      st.toast('Model table downloaded!')
  st.markdown('📌 As colunas são :green-background[ORIGEM | DESTINO | SAP | VEICULO | FRETE], e :red-background[acusarão erro] caso não estejam neste formato')
  st.dataframe(model, hide_index=True, column_config=model_table_column_config())

  st.text('')

  st.subheader('Formatos aceitos para os campos de ORIGEM')
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

  st.text('')

  st.subheader("Tratamento de duplicatas nos ID's")
  st.markdown("📌 Rate Geo e Rate Geo Cost Group terão as :blue-background[duplicatas removidas] no :green-background[agrupamento ORIGEM + SAP + VEICULO], para :red-background[evitar o cadastro de dois ID's iguais]")
  col1, col2, col3, col4, col5 = st.columns([1.25, 0.2, 1, 0.2, 1.25])
  with col1:
    st.dataframe(model3, hide_index=True, column_config=doc_frete_column_config())
  with col2:
    st.text('');  st.text('');  st.text('');  st.text('')
    st.markdown('➡️➡️')
  with col3:
    st.dataframe(model3[['📍 ORIGEM', '🏷️ SAP', '🚚 VEICULO']], hide_index=True, column_config=doc_duplicate_table_column_config())
  with col4:
    st.text('');  st.text('');  st.text('');  st.text('')
    st.markdown('➡️➡️')
  with col5:
    st.text('');  st.text('')
    st.dataframe(model4, hide_index=True)

  st.text('')

  st.subheader('Dicionário de Origens')
  st.markdown('📌 Lista completa das :green-background[origens cadastradas no sistema] - formato :blue-background[SAP → OTM]')
  origens_df = get_origens_df()
  st.dataframe(origens_df, hide_index=True, use_container_width=True)
  st.markdown('📌 :orange-background[Contato com SupriLog] necessário para adição de novas origens')

  st.text('')

  st.subheader('Especificidade das tabelas por Unidade de Negócio')
  st.markdown('📌 As tabelas geradas contemplam a as :green-background[particularidades de cada Unidade de Negócio], sendo possível de :blue-background[selecionar a UN desejada]')
  col1, col2 = st.columns([3, 7])
  with col1:
    st.selectbox('Escolha a Unidade de Negócio:', ('UNPE', 'UNBC', 'UNC'))
  st.markdown('📌 :blue-background[Procurar o responsável da UN] pelos cadastros no OTM :green-background[em caso de dúvidas]')