import pandas as pd
import numpy as np

from otm_core.dicts import origens_mult, min_ton
from otm_core.calculations import DROP_INPUT_COLUMNS


def suz_mult(model):
  mult = model.copy()
  mult = mult[mult['X_LANE_GID'].str.replace('SUZANO.', '').str.replace('_BRA', '').isin(origens_mult)]

  mult['RATE_OFFERING_GID'] = mult['RATE_OFFERING_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult['RATE_GEO_DESC']     = 'MULT'
  mult['RATE_GEO_GID']      = mult['RATE_GEO_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult['RATE_GEO_XID']      = mult['RATE_GEO_XID'].str.replace('UNPE', 'UNPE_MULT')

  model = pd.concat([model, mult], ignore_index=True)
  return model

def multicoleta(model):
  mult_ne = model[model['ORIGEM'].isin(origens_mult)].copy()
  mult_eq = model[model['ORIGEM'].isin(origens_mult)].copy()

  mult_ne['RATE_GEO_COST_GROUP_GID'] = mult_ne['RATE_GEO_COST_GROUP_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult_ne['MIN_COST_CURRENCY_GID']   = np.nan
  mult_ne['ATTRIBUTE_NUMBER1']       = mult_ne['VEICULO'].map(min_ton) * 100
  mult_ne['LEFT_OPERAND3']           = 'SHIPMENT.FLEX_ATTRIBUTE10'
  mult_ne['LOW_VALUE3']              = 'SIM'
  mult_ne['OPER3_GID']               = 'NE'
  mult_ne['MIN_COST']                = np.nan
  mult_ne['AND_OR2']                 = 'A'

  mult_eq['RATE_GEO_COST_GROUP_GID'] = mult_eq['RATE_GEO_COST_GROUP_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult_eq['MIN_COST_CURRENCY_GID']   = np.nan
  mult_eq['ATTRIBUTE_NUMBER1']       = mult_eq['VEICULO'].map(min_ton) * 100
  mult_eq['CHARGE_QUALIFIER1']       = 'attributeNumber10'
  mult_eq['CHARGE_MULTIPLIER']       = 'SHIPMENT.FLEX_FIELD_N_WEIGHT'
  mult_eq['LEFT_OPERAND3']           = 'SHIPMENT.FLEX_ATTRIBUTE10'
  mult_eq['LOW_VALUE3']              = 'SIM'
  mult_eq['OPER3_GID']               = 'EQ'
  mult_eq['MIN_COST']                = np.nan
  mult_eq['AND_OR2']                 = 'A'

  mults                      = pd.concat([mult_ne, mult_eq], ignore_index=True)
  mults['ATTRIBUTE_NUMBER1'] = pd.to_numeric(mults['ATTRIBUTE_NUMBER1'], errors='coerce').astype('Int64')
  model                      = pd.concat([model, mults.drop(columns=DROP_INPUT_COLUMNS)], ignore_index=True)

  return model
