import pandas as pd
import numpy as np

from dicts import origens_mult, origens, equipms_unpe, equipms_unbc, veiculos_unbc, min_ton

def not_mapped_check(model):
  not_mapped               = model.copy()
  not_mapped['NOT_MAPPED'] = not_mapped['ORIGEM'].map(origens)
  not_mapped               = not_mapped[not_mapped['NOT_MAPPED'].isna()]
  not_mapped               = not_mapped.rename_axis('Index')
  not_mapped               = not_mapped['ORIGEM']
  return not_mapped

def suz_mult(model):
  mult = model.copy()
  mult = mult[mult['X_LANE_GID'].str.replace('SUZANO.', '').str.replace('_BRA', '').isin(origens_mult)]

  mult['RATE_OFFERING_GID'] = mult['RATE_OFFERING_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult['RATE_GEO_GID']      = mult['RATE_GEO_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult['RATE_GEO_XID']      = mult['RATE_GEO_XID'].str.replace('UNPE', 'UNPE_MULT')

  model = pd.concat([model, mult], ignore_index=True)
  return model

def rate_offering_gid(model, unity, equipms):
  model['EQUIPMENT_GROUP_PROFILE_GID'] = model.apply(lambda row: 
    f"{equipms.get(row['VEICULO'], '')}_CD_SUZANO" if row['ORIGEM'] == 'SSUZ' or row['ORIGEM'] == 'CDL_SUZ_1112' # row['ORIGEM'] in origens_suz
    else equipms.get(row['VEICULO'], ''), axis=1)

  model['RATE_OFFERING_GID'] = model.apply(lambda row: 
  f'SUZANO.{unity}_0000{row["SAP"]}_CD_SUZANO' if row['ORIGEM'] == 'SSUZ' or row['ORIGEM'] == 'CDL_SUZ_1112' # row['ORIGEM'] in origens_suz
  else f'SUZANO.{unity}_0000{row["SAP"]}', axis=1)

  return model

def build_model_rg(model, unity):
  model['FLEX_COMMODITY_PROFILE_GID']  = f'SUZANO.COP_{unity}'
  model['ALLOW_UNCOSTED_LINE_ITEMS']   = 'N'
  model['IS_MASTER_OVERRIDES_BASE']    = 'N'
  model['MULTI_BASE_GROUPS_RULE']      = 'A'
  model['ROUNDING_FIELDS_LEVEL']       = '0'
  model['ROUNDING_APPLICATION']        = 'A'
  model['HAZARDOUS_RATE_TYPE']         = 'A'
  model['IS_SOURCING_RATE']            = 'N'
  model['IS_FROM_BEYOND']              = 'Y'
  model['RATE_GEO_DESC']               = 'SAW'
  model['IS_FOR_BEYOND']               = 'Y'
  model['ROUNDING_TYPE']               = 'N'
  model['DOMAIN_NAME']                 = 'SUZANO'
  model['X_LANE_GID']                  = 'SUZANO.' + model['ORIGEM'].map(origens) + '_BRA'
  model['IS_QUOTE']                    = 'N'

  if unity == 'UNPE':
    equipms = equipms_unpe
    model['RATE_GEO_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
  elif unity == 'UNBC':
    equipms = equipms_unbc
    model['RATE_GEO_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  elif unity == 'UNC':
    model['RATE_GEO_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  if unity != 'UNC':
    model = rate_offering_gid(model, unity, equipms)

  model                 = model[~model['RATE_GEO_GID'].isna()]
  model['RATE_GEO_XID'] = model['RATE_GEO_GID'].str.replace('SUZANO.', '')

  ## Adding mult to UNPE ##
  if unity == 'UNPE':
    model = suz_mult(model)

  return model

def min_cost_calculation(model, unity):
  if unity == 'UNC':
    model['MIN_COST'] = model.apply(lambda row: row['CHARGE_AMOUNT'] * 25, axis=1)
  else:
    model['MIN_COST'] = model.apply(lambda row: row['CHARGE_AMOUNT'] * min_ton[row['VEICULO']], axis=1)
  model['MIN_COST']              = model['MIN_COST'].round(2)
  model['MIN_COST_CURRENCY_GID'] = 'BRL'
  return model

def format_date():
  from datetime import datetime, timedelta

  current_date = datetime.now()
  one_day_ago  = current_date - timedelta(days=1)
  format_date  = one_day_ago.strftime('%Y%m%d') + '030000'
  return format_date

def rate_geo_cost_cols(model):
  model['EFFECTIVE_DATE'] = format_date()
  model['CHARGE_AMOUNT']  = model['CHARGE_AMOUNT'].round(2)
  model['LOW_VALUE2']     = model['DESTINO'].apply(lambda x: f'SUZANO.{x}')

  model['CHARGE_MULTIPLIER_OPTION'] = 'A'
  model['ALLOW_ZERO_RBI_VALUE']     = 'N'
  model['CHARGE_CURRENCY_GID']      = 'BRL'
  model['IS_FILED_AS_TARIFF']       = 'N'
  model['CHARGE_UNIT_COUNT']        = '1'
  model['LEFT_OPERAND1']            = 'SHIPMENT.STOPS.SHIPUNITS.ACTIVITY'
  model['LEFT_OPERAND2']            = 'SHIPMENT.DEST.REGION'
  model['CHARGE_ACTION']            = 'A'
  model['CHARGE_TYPE']              = 'B'
  model['DOMAIN_NAME']              = 'SUZANO'
  model['LOW_VALUE1']               = 'D'
  model['OPER1_GID']                = 'EQ'
  model['OPER2_GID']                = 'EQ'
  model['COST_TYPE']                = 'C'
  model['AND_OR1']                  = 'A'

  return model

def multicoleta(model):
  mult_ne = model[model['ORIGEM'].isin(origens_mult)].copy()
  mult_eq = model[model['ORIGEM'].isin(origens_mult)].copy()

  columns_mult = ['RATE_GEO_COST_GROUP_GID', 'RATE_GEO_COST_SEQ', 'DESCRIPTION', 'TARIFF_ITEM_NUMBER', 'TARIFF_SECTION', 'TARIFF_ITEM_NUMBER_SUFFIX', 'TARIFF_ITEM_PART', 'TARIFF_FREIGHT_CLASS_CODE', 'EX_PARTE', 'RATE_BASIS_NUMBER', 'TARIFF_COLUMN', 'TARIFF_DISTANCE', 'TARIFF_DISTANCE_UOM_CODE', 'TARIFF_DISTANCE_BASE', 'DISTANCE_QUALIFIER', 'RATE_BASIS_QUALIFIER', 'RATE_GEO_COST_OPERAND_SEQ', 'OPER1_GID', 'LEFT_OPERAND1', 'LOW_VALUE1', 'HIGH_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'HIGH_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'HIGH_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_AMOUNT_BASE', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_MULTIPLIER_SCALAR', 'CHARGE_ACTION', 'CHARGE_BREAK_COMPARATOR', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'CHARGE_MULTIPLIER2', 'CHARGE_UNIT_COUNT2', 'CHARGE_UNIT_UOM_CODE2', 'CHARGE_SEQUENCE', 'DIM_RATE_FACTOR_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'MIN_COST_BASE', 'MAX_COST', 'MAX_COST_CURRENCY_GID', 'MAX_COST_BASE', 'PAYMENT_METHOD_CODE_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'CALENDAR_GID', 'IS_FILED_AS_TARIFF', 'TIER', 'COST_TYPE', 'CALENDAR_ACTIVITY_GID', 'RATE_UNIT_BREAK_PROFILE_GID', 'RATE_UNIT_BREAK_PROFILE2_GID', 'CHARGE_BREAK_COMPARATOR2_GID', 'EXTERNAL_RATING_ENGINE_GID', 'EXT_RE_FIELDSET_GID', 'COST_CODE_GID', 'LOGIC_PARAM_QUAL_GID', 'COST_CATEGORY_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE6', 'ATTRIBUTE7', 'ATTRIBUTE8', 'ATTRIBUTE9', 'ATTRIBUTE10', 'ATTRIBUTE11', 'ATTRIBUTE12', 'ATTRIBUTE13', 'ATTRIBUTE14', 'ATTRIBUTE15', 'ATTRIBUTE16', 'ATTRIBUTE17', 'ATTRIBUTE18', 'ATTRIBUTE19', 'ATTRIBUTE20', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER5', 'ATTRIBUTE_NUMBER6', 'ATTRIBUTE_NUMBER7', 'ATTRIBUTE_NUMBER8', 'ATTRIBUTE_NUMBER9', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ATTRIBUTE_DATE6', 'ATTRIBUTE_DATE7', 'ATTRIBUTE_DATE8', 'ATTRIBUTE_DATE9', 'ATTRIBUTE_DATE10', 'ALLOW_ZERO_RBI_VALUE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'OPERAND_QUALIFIER1', 'OPERAND_QUALIFIER2', 'OPERAND_QUALIFIER3', 'OPERAND_QUALIFIER4', 'CHARGE_QUALIFIER1', 'CHARGE_QUALIFIER2', 'CHARGE_BREAK_COMP_QUALIFIER1', 'CHARGE_BREAK_COMP_QUALIFIER2', 'DOMAIN_NAME']
  new_row_mult = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"] + [np.nan] * (len(columns_mult) - 1)], columns=columns_mult)
  df_mults     = pd.concat([new_row_mult, pd.DataFrame(columns=columns_mult)], ignore_index=True)

  mult_ne['RATE_GEO_COST_GROUP_GID'] = mult_ne['RATE_GEO_COST_GROUP_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult_ne['MIN_COST_CURRENCY_GID']   = np.nan
  mult_ne['ATTRIBUTE_NUMBER1']       = model.apply(lambda row: min_ton[row['VEICULO']] * 100, axis=1)
  mult_ne['LEFT_OPERAND3']           = 'SHIPMENT.FLEX_ATTRIBUTE10'
  mult_ne['LOW_VALUE3']              = 'SIM'
  mult_ne['OPER3_GID']               = 'NE'
  mult_ne['MIN_COST']                = np.nan
  mult_ne['AND_OR2']                 = 'A'

  mult_eq['RATE_GEO_COST_GROUP_GID'] = mult_eq['RATE_GEO_COST_GROUP_GID'].str.replace('UNPE', 'UNPE_MULT')
  mult_eq['MIN_COST_CURRENCY_GID']   = np.nan
  mult_eq['ATTRIBUTE_NUMBER1']       = model.apply(lambda row: min_ton[row['VEICULO']] * 100, axis=1)
  mult_eq['CHARGE_QUALIFIER1']       = 'attributeNumber10'
  mult_eq['CHARGE_MULTIPLIER']       = 'SHIPMENT.FLEX_FIELD_N_WEIGHT'
  mult_eq['LEFT_OPERAND3']           = 'SHIPMENT.FLEX_ATTRIBUTE10'
  mult_eq['LOW_VALUE3']              = 'SIM'
  mult_eq['OPER3_GID']               = 'EQ'
  mult_eq['MIN_COST']                = np.nan
  mult_eq['AND_OR2']                 = 'A'

  mults                      = pd.concat([mult_ne, mult_eq], ignore_index=True)
  mults['ATTRIBUTE_NUMBER1'] = pd.to_numeric(mults['ATTRIBUTE_NUMBER1'], errors='coerce').astype('Int64')
  df_mults                   = pd.concat([df_mults, mults.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)

  new_row   = pd.DataFrame([['RATE_GEO_COST'] + [np.nan] * (df_mults.shape[1] - 1)], columns=df_mults.columns)
  df_header = pd.concat([new_row, df_mults], ignore_index=True)

  new_header        = df_header.iloc[0]
  df_header         = df_header[1:]
  df_header.columns = new_header
  old_header        = pd.DataFrame([df_mults.columns], columns=df_header.columns)
  df_mults          = pd.concat([old_header, df_header], ignore_index=True)

  return df_mults