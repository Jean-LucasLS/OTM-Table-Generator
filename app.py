import streamlit as st
import pandas as pd
import numpy as np

from otm_generator import rate_geo, rate_geo_cost_ton, rate_geo_cost_viagem

from io import BytesIO

def to_excel(df):
  output = BytesIO()
  writer = pd.ExcelWriter(output, engine='xlsxwriter')
  df.to_excel(writer, index=False, sheet_name='Sheet1')
  writer.close()
  processed_data = output.getvalue()
  return processed_data

st.set_page_config(page_title='OTM Table Generator', page_icon='📊', layout='wide')

# Função principal para rodar a aplicação
def main():
  st.header(body='OTM Table Generator per Unity - SupriLog')
  st.text('')
  st.text('')

  # Lista suspensa para escolher a Unidade de Negócio
  col1, col2, col3, col4 = st.columns([3, 6, 1.25, 1])
  with col1:
    unity = st.selectbox('Choose the Unity:', ('UNPE', 'UNBC', 'UNC'))
  with col3:
    st.markdown('📥 :rainbow[Download the model table here] ➡️')
  with col4:
    model = pd.DataFrame({'ORIGEM': ['FSCB'], 'DESTINO': ['L123456789'], 'SAP': [123456], 'VEICULO': ['Y06'], 'FRETE': [44.44]})
    model = to_excel(model)
    if st.download_button(label='model.xlsx', data=model, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download the model table used for upload'):
      st.toast('Model table downloaded!')

  st.text('')

  # Opções de flag para executar funções
  col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 4])
  with col1:
    rate_geo_flag = st.checkbox('Rate Geo')
  with col2:
    rate_geo_cost_group_flag = st.checkbox('Rate Geo Cost Group')
  with col3:
    rate_geo_cost_viagem_flag = st.checkbox('Rate Geo Cost (Viagem)')
  with col4:
    if unity == 'UNPE' or unity == 'UNC':
      rate_geo_cost_ton_flag = st.checkbox('Rate Geo Cost (ton)')
      if unity == 'UNC' and rate_geo_cost_ton_flag:
        min_cost_flag = st.checkbox('min_cost')
    else:
      rate_geo_cost_ton_flag = False
  st.text("")

  # Botão para upload de arquivo
  col1, col2 = st.columns([2, 4])
  with col1:
    df_path = st.file_uploader('Choose a .xlsx or .csv file', type=['xlsx', 'csv'])

  if df_path is not None:
    # Leitura do arquivo
    if df_path.name.endswith('.xlsx'):
      df = pd.read_excel(df_path)
    else:
      df = pd.read_csv(df_path)
    df['SAP'] = df['SAP'].astype(str)

    # Verificar flags e exibir botões de download
    col1, col2, col3, col4, col5 = st.columns([0.75, 1, 1.25, 1, 4])
    if rate_geo_flag or rate_geo_cost_group_flag:
      csv_rate_geo, csv_rate_geo_cost_group = rate_geo(model=df, unity=unity)
      if rate_geo_flag:
        with col1:
          st.download_button(label='Rate Geo', data=csv_rate_geo, file_name='rate_geo.csv', mime='text/csv')
      if rate_geo_cost_group_flag:
        with col2:
          st.download_button(label='Rate Geo Cost Group', data=csv_rate_geo_cost_group, file_name='rate_geo_cost_group.csv', mime='text/csv')
    if rate_geo_cost_viagem_flag:
      csv_rate_geo_cost_viagem = rate_geo_cost_viagem(model=df, unity=unity)
      with col3:
        st.download_button(label='Rate Geo Cost (viagem)', data=csv_rate_geo_cost_viagem, file_name='rate_geo_cost_viagem.csv', mime='text/csv')
    if rate_geo_cost_ton_flag:
      csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df, unity=unity, min_cost=min_cost_flag)
      with col4:
        st.download_button(label='Rate Geo Cost (ton)', data=csv_rate_geo_cost_ton, file_name='rate_geo_cost_ton.csv', mime='text/csv')



    # Exibição do DataFrame
    st.write('')
    st.dataframe(df, hide_index=True,
                column_config={
                'ORIGEM': st.column_config.TextColumn(label='📍 ORIGEM'),
                'DESTINO': st.column_config.TextColumn(label='🎯 DESTINO'),
                'SAP': st.column_config.TextColumn(label='🏷️ SAP'),
                'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO'),
                'FRETE': st.column_config.NumberColumn(label='💸 FRETE', format='%.2f R$')
                })

if __name__ == '__main__':
  main()
