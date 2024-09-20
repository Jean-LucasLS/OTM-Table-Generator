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
  mult['RATE_GEO_DESC']     = 'MULT'
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
  columns_rg = ['RATE_GEO_GID', 'RATE_GEO_XID', 'RATE_OFFERING_GID', 'X_LANE_GID', 'EQUIPMENT_GROUP_PROFILE_GID', 'RATE_SERVICE_GID', 'MIN_COST', 'MIN_COST_GID', 'MIN_COST_BASE', 'TOTAL_STOPS_CONSTRAINT', 'PICKUP_STOPS_CONSTRAINT', 'DELIVERY_STOPS_CONSTRAINT', 'CIRCUITY_ALLOWANCE_PERCENT', 'CIRCUITY_DISTANCE_COST', 'CIRCUITY_DISTANCE_COST_GID', 'CIRCUITY_DISTANCE_COST_BASE', 'MAX_CIRCUITY_PERCENT', 'MAX_CIRCUITY_DISTANCE', 'MAX_CIRCUITY_DISTANCE_UOM_CODE', 'MAX_CIRCUITY_DISTANCE_BASE', 'STOPS_INCLUDED_RATE', 'FLEX_COMMODITY_PROFILE_GID', 'RATE_QUALITY_GID', 'SHIPPER_MIN_VALUE', 'MIN_STOPS', 'SHORT_LINE_COST', 'SHORT_LINE_COST_GID', 'SHORT_LINE_COST_BASE', 'RATE_ZONE_PROFILE_GID', 'LOCATION_GID', 'ROUTE_CODE_GID', 'DIM_RATE_FACTOR_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'ALLOW_UNCOSTED_LINE_ITEMS', 'SHIPPER_MIN_VALUE_GID', 'MULTI_BASE_GROUPS_RULE', 'RAIL_INTER_MODAL_PLAN_GID', 'CUSTOMER_RATE_CODE', 'COFC_TOFC', 'EXPIRE_MARK_ID', 'VIA_SRC_LOC_PROF_GID', 'VIA_DEST_LOC_PROF_GID', 'VIA_SRC_LOC_GID', 'VIA_DEST_LOC_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'BUY_SERVPROV_PROFILE_GID', 'BUY_RATE_GEO_PROFILE_GID', 'PAYMENT_METHOD_CODE_GID', 'IS_MASTER_OVERRIDES_BASE', 'HAZARDOUS_RATE_TYPE', 'IS_QUOTE', 'DOMAIN_PROFILE_GID', 'RO_TIME_PERIOD_DEF_GID', 'LOGIC_CONFIG_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE6', 'ATTRIBUTE7', 'ATTRIBUTE8', 'ATTRIBUTE9', 'ATTRIBUTE11', 'ATTRIBUTE12', 'ATTRIBUTE13', 'ATTRIBUTE14', 'ATTRIBUTE15', 'ATTRIBUTE16', 'ATTRIBUTE17', 'ATTRIBUTE18', 'ATTRIBUTE19', 'ATTRIBUTE20', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER5', 'ATTRIBUTE_NUMBER6', 'ATTRIBUTE_NUMBER7', 'ATTRIBUTE_NUMBER8', 'ATTRIBUTE_NUMBER9', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ATTRIBUTE_DATE6', 'ATTRIBUTE_DATE7', 'ATTRIBUTE_DATE8', 'ATTRIBUTE_DATE9', 'ATTRIBUTE_DATE10', 'RATE_GEO_DESC', 'IS_FOR_BEYOND', 'IS_FROM_BEYOND', 'CORPORATION_PROFILE_GID', 'PARENT_RATE_GEO_GID', 'IS_SOURCING_RATE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'DOMAIN_NAME']
  new_row    = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'"] + [np.nan] * (len(columns_rg) - 1)], columns=columns_rg)
  df_rg      = pd.concat([new_row, pd.DataFrame(columns=columns_rg)], ignore_index=True)
  model      = model.drop_duplicates(subset=['ORIGEM', 'SAP', 'VEICULO'], keep='first')

  if unity == 'UNPE_CABOTAGEM':
    unity_name = 'UNPE'
  else:
    unity_name = unity

  model['FLEX_COMMODITY_PROFILE_GID']  = f'SUZANO.COP_{unity_name}'
  model['ALLOW_UNCOSTED_LINE_ITEMS']   = 'N'
  model['IS_MASTER_OVERRIDES_BASE']    = 'N'
  model['MULTI_BASE_GROUPS_RULE']      = 'A'
  model['ROUNDING_FIELDS_LEVEL']       = '0'
  model['ROUNDING_APPLICATION']        = 'A'
  model['HAZARDOUS_RATE_TYPE']         = 'A'
  model['RATE_OFFERING_GID']           = f'SUZANO.{unity_name}_0000' + model['SAP'].astype(str)
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
  elif unity == 'UNPE_CABOTAGEM':
    model['RATE_GEO_GID'] = f'SUZANO.{unity_name}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)
  elif unity == 'UNBC':
    equipms = equipms_unbc
    model['RATE_GEO_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  elif unity == 'UNC':
    model['RATE_GEO_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  if unity != 'UNC' and unity != 'UNPE_CABOTAGEM':
    model = rate_offering_gid(model, unity, equipms)

  model                 = model[~model['RATE_GEO_GID'].isna()]
  model['RATE_GEO_XID'] = model['RATE_GEO_GID'].str.replace('SUZANO.', '')

  ## Adding mult to UNPE ##
  if unity == 'UNPE':
    model = suz_mult(model)

  rate_geo = pd.concat([df_rg, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO', 'FRETE'])], ignore_index=True)
  return rate_geo, model

def build_model_rgcg(model, unity):
  columns_rgcg = ['RATE_GEO_COST_GROUP_GID', 'RATE_GEO_COST_GROUP_XID', 'RATE_GEO_GID', 'GROUP_NAME', 'DEFICIT_CALCULATIONS_TYPE', 'MULTI_RATES_RULE', 'RATE_GROUP_TYPE', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DOMAIN_NAME']
  new_row      = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'"] + [np.nan] * (len(columns_rgcg) - 1)], columns=columns_rgcg)
  df_rgcg      = pd.concat([new_row, pd.DataFrame(columns=columns_rgcg)], ignore_index=True)
  modelcg      = pd.DataFrame(columns=columns_rgcg)

  modelcg['RATE_GEO_COST_GROUP_GID'] = model['RATE_GEO_GID'].copy()
  modelcg['RATE_GEO_COST_GROUP_XID'] = model['RATE_GEO_XID'].copy()
  modelcg['ROUNDING_APPLICATION']    = 'A'
  modelcg['MULTI_RATES_RULE']        = 'X'
  modelcg['RATE_GROUP_TYPE']         = 'M'
  modelcg['ROUNDING_TYPE']           = 'N'
  modelcg['RATE_GEO_GID']            = model['RATE_GEO_GID'].copy()
  modelcg['DOMAIN_NAME']             = 'SUZANO'

  if unity == 'UNPE':
    modelcg['MULTI_RATES_RULE'] = np.where(modelcg['RATE_GEO_COST_GROUP_XID'].str[:9] == 'UNPE_MULT', 'A', 'X')

  rate_geo_cost_group = pd.concat([df_rgcg, modelcg], ignore_index=True)
  return rate_geo_cost_group

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
  model = model.rename(columns={'FRETE': 'CHARGE_AMOUNT'})
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
  model                      = pd.concat([model, mults.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)

  return model

def df_rgcv_cols(model, unity):
  columns_rgcv  = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID' ,'LEFT_OPERAND1', 'LOW_VALUE1', 'HIGH_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'HIGH_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'HIGH_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_AMOUNT_BASE', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_MULTIPLIER_SCALAR', 'CHARGE_ACTION', 'CHARGE_BREAK_COMPARATOR', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'CHARGE_MULTIPLIER2', 'CHARGE_UNIT_COUNT2', 'CHARGE_UNIT_UOM_CODE2', 'CHARGE_SEQUENCE', 'DIM_RATE_FACTOR_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'MIN_COST_BASE', 'MAX_COST', 'MAX_COST_CURRENCY_GID', 'MAX_COST_BASE', 'PAYMENT_METHOD_CODE_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'CALENDAR_GID', 'IS_FILED_AS_TARIFF', 'TIER', 'COST_TYPE', 'CALENDAR_ACTIVITY_GID', 'RATE_UNIT_BREAK_PROFILE_GID', 'RATE_UNIT_BREAK_PROFILE2_GID', 'CHARGE_BREAK_COMPARATOR2_GID', 'EXTERNAL_RATING_ENGINE_GID', 'EXT_RE_FIELDSET_GID', 'COST_CODE_GID', 'LOGIC_PARAM_QUAL_GID', 'COST_CATEGORY_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ALLOW_ZERO_RBI_VALUE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'OPERAND_QUALIFIER1', 'OPERAND_QUALIFIER2', 'OPERAND_QUALIFIER3', 'OPERAND_QUALIFIER4', 'CHARGE_QUALIFIER1', 'CHARGE_QUALIFIER2', 'CHARGE_BREAK_COMP_QUALIFIER1', 'CHARGE_BREAK_COMP_QUALIFIER2', 'DOMAIN_NAME']
  new_row       = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS'"] + [np.nan] * (len(columns_rgcv) - 1)], columns=columns_rgcv)
  df_rgcv       = pd.concat([new_row, pd.DataFrame(columns=columns_rgcv)], ignore_index=True)

  if unity == 'UNPE':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
  if unity == 'UNPE_CABOTAGEM':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.UNPE_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)
  if unity == 'UNBC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  if unity == 'UNC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  model                      = rate_geo_cost_cols(model)
  model['CHARGE_MULTIPLIER'] = 'SHIPMENT'
  if unity == 'UNPE':
    model = multicoleta(model)

  rate_geo_cost_viagem = pd.concat([df_rgcv, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)
  rate_geo_cost_viagem = rate_geo_cost_viagem[~rate_geo_cost_viagem['RATE_GEO_COST_GROUP_GID'].isna()]
  return rate_geo_cost_viagem