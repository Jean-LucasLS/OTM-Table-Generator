import streamlit as st


def model_table_column_config():
  return {
    'ORIGEM': st.column_config.TextColumn(label='📍 ORIGEM'),
    'DESTINO': st.column_config.TextColumn(label='🎯 DESTINO'),
    'SAP': st.column_config.TextColumn(label='🏷️ SAP'),
    'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO'),
    'FRETE': st.column_config.NumberColumn(label='💸 FRETE', format='%.2f R$'),
  }


def not_mapped_column_config():
  return {
    'Index': st.column_config.TextColumn(label='Index'),
    'ORIGEM': st.column_config.TextColumn(label='⚠️ ORIGEM'),
  }


def doc_duplicate_table_column_config():
  return {
    'SAP': st.column_config.TextColumn(label='🏷️ DESTINO'),
    'VEICULO': st.column_config.TextColumn(label='🚚 VEICULO'),
  }


def doc_frete_column_config():
  return {
    '💸 FRETE': st.column_config.NumberColumn(format='%.2f R$'),
  }
