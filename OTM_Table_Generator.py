import pandas as pd
import streamlit as st

from otm_core.otm_generator import rate_geo, rate_geo_cost_ton, rate_geo_cost_viagem
from ui.excel_utils import to_excel
from ui.table_configs import get_template_model_df, model_table_column_config, not_mapped_column_config


def main():
  col1, col2, col3,= st.columns([3, 5, 2], vertical_alignment='bottom', horizontal_alignment='right')
  with col1:
    unity = st.selectbox('Escolha a Unidade de Negócio:', ('UNPE', 'UNPE_CABOTAGEM', 'UNBC', 'UNC', 'UNTS'))
  with col3:
    model = get_template_model_df()
    model = to_excel(model)
    if st.download_button(label='📥 model.xlsx', data=model, file_name='model.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', help='Download da tabela modelo', key='model_download_generator'):
      st.toast('Model table downloaded!')

  st.text(''); col1, col2 = st.columns([2, 2])
  with col1:
    df_path = st.file_uploader('Escolha um arquivo .xlsx ou .csv', type=['xlsx', 'csv'])

  if df_path is not None:
    if df_path.name.endswith('.xlsx'):
      df = pd.read_excel(df_path)
    else:
      df = pd.read_csv(df_path)
    df['SAP'] = df['SAP'].astype(str)

    col1, col2, col3, col4, col5, _ = st.columns([0.75, 1, 1, 0.8, 1, 2])
    if unity == 'UNPE':
      with col5:
        mult_flag = st.checkbox('mult')
      csv_rate_geo, csv_rate_geo_cost_group, not_mapped = rate_geo(model=df.copy(), unity=unity, mult_flag=mult_flag)
    elif unity == 'UNBC':
      with col4:
        opl_flag = st.checkbox('OPL')
      csv_rate_geo, csv_rate_geo_cost_group, not_mapped = rate_geo(model=df.copy(), unity=unity, opl_flag=opl_flag)
      
    else:
      csv_rate_geo, csv_rate_geo_cost_group, not_mapped = rate_geo(model=df.copy(), unity=unity)
    with col1:
      if st.download_button(label='Rate Geo', data=csv_rate_geo, file_name='rate_geo.csv', mime='text/csv'):
        st.toast('Rate Geo table downloaded!')
    with col2:
      if st.download_button(label='Rate Geo Cost Group', data=csv_rate_geo_cost_group, file_name='rate_geo_cost_group.csv', mime='text/csv'):
        st.toast('Rate Geo Cost Group table downloaded!')
    with col3:
      if unity == 'UNBC':
        csv_rate_geo_cost_viagem = rate_geo_cost_viagem(model=df.copy(), unity=unity, opl_flag=opl_flag)
      else:
        csv_rate_geo_cost_viagem = rate_geo_cost_viagem(model=df.copy(), unity=unity)
      if st.download_button(label='Rate Geo Cost (viagem)', data=csv_rate_geo_cost_viagem, file_name='rate_geo_cost_viagem.csv', mime='text/csv'):
        st.toast('Rate Geo Cost (viagem) table downloaded!')
    with col4:
      if unity not in ['UNBC', 'UNPE_CABOTAGEM', 'UNTS']:
        csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df.copy(), unity=unity, min_cost=True)
      if unity == 'UNPE':
        csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df.copy(), unity=unity, min_cost=True, mult_flag=mult_flag)
        if st.download_button(label='Rate Geo Cost (ton)', data=csv_rate_geo_cost_ton, file_name='rate_geo_cost_ton.csv', mime='text/csv'):
          st.toast('Rate Geo Cost (ton) table downloaded!')
    if unity == 'UNC':
      with col5:
        min_cost_flag         = st.checkbox('min_cost')
        csv_rate_geo_cost_ton = rate_geo_cost_ton(model=df.copy(), unity=unity, min_cost=min_cost_flag)
      if st.download_button(label='Rate Geo Cost (ton)', data=csv_rate_geo_cost_ton, file_name='rate_geo_cost_ton.csv', mime='text/csv'):
        st.toast('Rate Geo Cost (ton) table downloaded!')

    st.text(''); col1, col2 = st.columns(2)
    with col1:
      st.text(''); st.dataframe(df, hide_index=True, column_config=model_table_column_config())
    with col2:
      if not_mapped.shape[0] != 0:
        st.text(''); st.write('❗ Not-mapped origins')
        st.dataframe(not_mapped, column_config=not_mapped_column_config())

if __name__ == '__main__':
  main()
