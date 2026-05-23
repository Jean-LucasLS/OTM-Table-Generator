import pandas as pd


def get_template_model_df():
  return pd.DataFrame({
    'ORIGEM': ['FSCB', 'FAB_SUZ_1101'],
    'DESTINO': ['L123456789', 'L123456789'],
    'SAP': [123456, 123456],
    'VEICULO': ['Y06', 'Y06'],
    'FRETE': [44.44, 44.44],
  })
