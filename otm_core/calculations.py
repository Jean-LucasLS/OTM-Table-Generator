import numpy as np
from datetime import datetime, timedelta

from otm_core.dicts import min_ton

DROP_INPUT_COLUMNS    = ['ORIGEM', 'DESTINO', 'SAP', 'VEICULO']
DROP_INPUT_WITH_FRETE = DROP_INPUT_COLUMNS + ['FRETE']
CD_SUZANO_ORIGENS     = ['SSUZ', 'CDL_SUZ_1112']


def min_cost_calculation(model, unity):
  if unity == 'UNC':
    model['MIN_COST'] = model['CHARGE_AMOUNT'] * 25
  else:
    model['MIN_COST'] = model['VEICULO'].map(min_ton) * model['CHARGE_AMOUNT']
  model['MIN_COST']              = model['MIN_COST'].round(2)
  model['MIN_COST_CURRENCY_GID'] = 'BRL'
  return model

def format_date():
  one_day_ago = datetime.now() - timedelta(days=1)
  return one_day_ago.strftime('%Y%m%d') + '030000'

def _filter_pe_m(df, col, mult_flag):
  mask = df[col].str.contains('PE_M', na=False)
  return df[mask] if mult_flag else df[~mask]

def direct_mult_split(model, mult_flag=False):
  return _filter_pe_m(model, 'RATE_GEO_GID', mult_flag)

def direct_mult_split_ton(rate_geo_cost_ton, mult_flag=False):
  return _filter_pe_m(rate_geo_cost_ton, 'RATE_GEO_COST_GROUP_GID', mult_flag)
