import numpy as np
import pandas as pd
import streamlit as st

from io import BytesIO
from otm_generator import rate_geo, rate_geo_cost_ton, rate_geo_cost_viagem

def to_excel(df):
  output = BytesIO()
  writer = pd.ExcelWriter(output, engine='xlsxwriter')
  df.to_excel(writer, index=False, sheet_name='Sheet1')
  writer.close()
  processed_data = output.getvalue()
  return processed_data

st.set_page_config(page_title='OTM Table Generator', page_icon='🤖', layout='wide')

def main():
  st.header(body='🗂️ OTM Table Generator - SupriLog 🗃️', divider='green')
  st.text('')
  st.text('')

  ## Unity drop-down list / Model (.xlsx) download ##
  col1, col2, col3, col4, col5 = st.columns([3, 1, 5, 1.25, 1])
  with col1:
    unity = st.selectbox('Choose the Unity:', ('UNPE', 'UNBC', 'UNC'))
  with col4:
    st.markdown('📥 :rainbow[Download the model table here] ➡️')
  with col5:
    model = pd.DataFrame({'ORIGEM': ['FSCB', 'FAB_SUZ_1101'], 'DESTINO': ['L123456789', 'L123456789'], 'SAP': [123456, 123456], 'VEICULO': ['Y06', 'Y06'], 'FRETE': [44.44, 44.44]})
    model = to_excel(model)
    if st.download_button(label='model.xlsx', data=model, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download the model table used for upload'):
      st.toast('Model table downloaded!')

  st.text('')

  ## Upload file button (.xlsx or .csv) ##
  col1, col2 = st.columns([2, 4])
  with col1:
    df_path = st.file_uploader('Choose a .xlsx or .csv file', type=['xlsx', 'csv'])

  ## Verifying file type and reading DataFrame ##
  if df_path is not None:
    if df_path.name.endswith('.xlsx'):
      df = pd.read_excel(df_path)
    else:
      df = pd.read_csv(df_path)
    df['SAP'] = df['SAP'].astype(str)

    ## Convert model into OTM Tables and create download buttons after file upload ##
    col1, col2, col3, col4, col5, col6 = st.columns([0.75, 1, 1, 0.8, 1, 2])
    with col1:
      csv_rate_geo, csv_rate_geo_cost_group = rate_geo(model=df, unity=unity)
      if st.download_button(label='Rate Geo', data=csv_rate_geo, file_name='rate_geo.csv', mime='text/csv'):
        st.toast('Rate Geo table downloaded!')
    with col2:
      if st.download_button(label='Rate Geo Cost Group', data=csv_rate_geo_cost_group, file_name='rate_geo_cost_group.csv', mime='text/csv'):
        st.toast('Rate Geo Cost Group table downloaded!')
    with col3:
      csv_rate_geo_cost_viagem = rate_geo_cost_viagem(model=df, unity=unity)
      if st.download_button(label='Rate Geo Cost (viagem)', data=csv_rate_geo_cost_viagem, file_name='rate_geo_cost_viagem.csv', mime='text/csv'):
        st.toast('Rate Geo Cost (viagem) table downloaded!')
    with col4:
      if unity != 'UNBC':
        csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df, unity=unity, min_cost=True)
        if unity == 'UNC':
          with col5:
            min_cost_flag = st.checkbox('min_cost')
            csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df, unity=unity, min_cost=min_cost_flag)
        if st.download_button(label='Rate Geo Cost (ton)', data=csv_rate_geo_cost_ton, file_name='rate_geo_cost_ton.csv', mime='text/csv'):
          st.toast('Rate Geo Cost (ton) table downloaded!')

    ## DataFrame view ##
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
