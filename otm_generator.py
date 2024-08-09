import pandas as pd
import numpy as np
from dicts import origens, origens_suz, equipms_unpe, equipms_unbc, veiculos_unbc,min_ton
from sat_funcs import not_mapped_check, build_model_rg, suz_mult

def rate_geo(model, unity):

  ## Not-mapped origins verifying ##
  not_mapped = not_mapped_check(model)

  ## Create rate_geo Dataframe ##
  columns_rg = ['RATE_GEO_GID', 'RATE_GEO_XID', 'RATE_OFFERING_GID', 'X_LANE_GID', 'EQUIPMENT_GROUP_PROFILE_GID', 'RATE_SERVICE_GID', 'MIN_COST', 'MIN_COST_GID', 'MIN_COST_BASE', 'TOTAL_STOPS_CONSTRAINT', 'PICKUP_STOPS_CONSTRAINT', 'DELIVERY_STOPS_CONSTRAINT', 'CIRCUITY_ALLOWANCE_PERCENT', 'CIRCUITY_DISTANCE_COST', 'CIRCUITY_DISTANCE_COST_GID', 'CIRCUITY_DISTANCE_COST_BASE', 'MAX_CIRCUITY_PERCENT', 'MAX_CIRCUITY_DISTANCE', 'MAX_CIRCUITY_DISTANCE_UOM_CODE', 'MAX_CIRCUITY_DISTANCE_BASE', 'STOPS_INCLUDED_RATE', 'FLEX_COMMODITY_PROFILE_GID', 'RATE_QUALITY_GID', 'SHIPPER_MIN_VALUE', 'MIN_STOPS', 'SHORT_LINE_COST', 'SHORT_LINE_COST_GID', 'SHORT_LINE_COST_BASE', 'RATE_ZONE_PROFILE_GID', 'LOCATION_GID', 'ROUTE_CODE_GID', 'DIM_RATE_FACTOR_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'ALLOW_UNCOSTED_LINE_ITEMS', 'SHIPPER_MIN_VALUE_GID', 'MULTI_BASE_GROUPS_RULE', 'RAIL_INTER_MODAL_PLAN_GID', 'CUSTOMER_RATE_CODE', 'COFC_TOFC', 'EXPIRE_MARK_ID', 'VIA_SRC_LOC_PROF_GID', 'VIA_DEST_LOC_PROF_GID', 'VIA_SRC_LOC_GID', 'VIA_DEST_LOC_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'BUY_SERVPROV_PROFILE_GID', 'BUY_RATE_GEO_PROFILE_GID', 'PAYMENT_METHOD_CODE_GID', 'IS_MASTER_OVERRIDES_BASE', 'HAZARDOUS_RATE_TYPE', 'IS_QUOTE', 'DOMAIN_PROFILE_GID', 'RO_TIME_PERIOD_DEF_GID', 'LOGIC_CONFIG_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE6', 'ATTRIBUTE7', 'ATTRIBUTE8', 'ATTRIBUTE9', 'ATTRIBUTE11', 'ATTRIBUTE12', 'ATTRIBUTE13', 'ATTRIBUTE14', 'ATTRIBUTE15', 'ATTRIBUTE16', 'ATTRIBUTE17', 'ATTRIBUTE18', 'ATTRIBUTE19', 'ATTRIBUTE20', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER5', 'ATTRIBUTE_NUMBER6', 'ATTRIBUTE_NUMBER7', 'ATTRIBUTE_NUMBER8', 'ATTRIBUTE_NUMBER9', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ATTRIBUTE_DATE6', 'ATTRIBUTE_DATE7', 'ATTRIBUTE_DATE8', 'ATTRIBUTE_DATE9', 'ATTRIBUTE_DATE10', 'RATE_GEO_DESC', 'IS_FOR_BEYOND', 'IS_FROM_BEYOND', 'CORPORATION_PROFILE_GID', 'PARENT_RATE_GEO_GID', 'IS_SOURCING_RATE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'DOMAIN_NAME']
  df_rg      = pd.DataFrame(columns=columns_rg)
  new_row    = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'"] + [np.nan] * (len(df_rg.columns) - 1)], columns=df_rg.columns)
  df_rg      = pd.concat([new_row, df_rg], ignore_index=True)
  
  ## Building a model to concat with rate_geo (df_rg) ##
  model = model.drop_duplicates(subset=['ORIGEM', 'SAP', 'VEICULO'], keep='first')
  model = build_model_rg(model, unity)

  rate_geo = pd.concat([df_rg, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO', 'FRETE'])], ignore_index=True)

  #### Creating rate_geo_cost_group (df_rgcg) based on rate_geo ####

  columns_rgcg = ['RATE_GEO_COST_GROUP_GID', 'RATE_GEO_COST_GROUP_XID', 'RATE_GEO_GID', 'GROUP_NAME', 'DEFICIT_CALCULATIONS_TYPE', 'MULTI_RATES_RULE', 'RATE_GROUP_TYPE', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DOMAIN_NAME']

  df_rgcg = pd.DataFrame(columns=columns_rgcg)
  modelcg = pd.DataFrame(columns=columns_rgcg)
  new_row = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'"] + [np.nan] * (len(df_rgcg.columns) - 1)], columns=df_rgcg.columns)
  df_rgcg = pd.concat([new_row, df_rgcg], ignore_index=True)

  modelcg['RATE_GEO_COST_GROUP_GID'] = model['RATE_GEO_GID']
  modelcg['RATE_GEO_COST_GROUP_XID'] = model['RATE_GEO_XID']
  modelcg['ROUNDING_APPLICATION']    = 'A'
  modelcg['MULTI_RATES_RULE']        = 'X'
  modelcg['RATE_GROUP_TYPE']         = 'M'
  modelcg['ROUNDING_TYPE']           = 'N'
  modelcg['RATE_GEO_GID']            = model['RATE_GEO_GID']
  modelcg['DOMAIN_NAME']             = 'SUZANO'

  if unity == 'UNPE':
    modelcg['MULTI_RATES_RULE'] = np.where(modelcg['RATE_GEO_COST_GROUP_XID'].str[:9] == 'UNPE_MULT', 'A', 'X')

  rate_geo_cost_group = pd.concat([df_rgcg, modelcg], ignore_index=True)

  rate_geo_csv            = rate_geo.to_csv(index=False)
  rate_geo_cost_group_csv = rate_geo_cost_group.to_csv(index=False)
  return rate_geo_csv, rate_geo_cost_group_csv, not_mapped

def rate_geo_cost_ton(model, unity, min_cost=True):
  model = model.rename(columns={'FRETE': 'CHARGE_AMOUNT'})

  #### Create rate_geo_cost Dataframe ####

  columns_rgct = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID', 'LEFT_OPERAND1', 'LOW_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_ACTION', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'IS_FILED_AS_TARIFF', 'COST_TYPE', 'ALLOW_ZERO_RBI_VALUE', 'OPERAND_QUALIFIER3', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'DOMAIN_NAME']
  df_rgct  = pd.DataFrame(columns=columns_rgct)
  new_row  = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS'"] + [np.nan] * (len(df_rgct.columns) - 1)], columns=df_rgct.columns)
  df_rgct  = pd.concat([new_row, df_rgct], ignore_index=True)

  #### Building a model to concat with rate_geo_cost (df_rgct) ####

  from datetime import datetime, timedelta

  current_date = datetime.now()
  one_day_ago  = current_date - timedelta(days=1)
  format_date  = one_day_ago.strftime('%Y%m%d') + '030000'

  if unity == 'UNPE':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
  if unity == 'UNBC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  if unity == 'UNC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  model['EFFECTIVE_DATE']          = format_date
  model['CHARGE_AMOUNT']           = model['CHARGE_AMOUNT'].round(2)
  model['LOW_VALUE2']              = model['DESTINO'].apply(lambda x: f'SUZANO.{x}')

  if min_cost:
    if unity == 'UNC':
     model['MIN_COST']                = model.apply(lambda row: row['CHARGE_AMOUNT'] * 25, axis=1)
    else:
      model['MIN_COST']               = model.apply(lambda row: row['CHARGE_AMOUNT'] * min_ton[row['VEICULO']], axis=1)
    model['MIN_COST']              = model['MIN_COST'].round(2)
    model['MIN_COST_CURRENCY_GID'] = 'BRL'

  model['CHARGE_MULTIPLIER_OPTION'] = 'A'
  model['CHARGE_UNIT_UOM_CODE']     = 'MTON'
  model['ALLOW_ZERO_RBI_VALUE']     = 'N'
  model['CHARGE_CURRENCY_GID']      = 'BRL'
  model['IS_FILED_AS_TARIFF']       = 'N'
  model['CHARGE_UNIT_COUNT']        = '1'
  model['CHARGE_MULTIPLIER']        = 'SHIPMENT.WEIGHT'
  model['LEFT_OPERAND1']            = 'SHIPMENT.STOPS.SHIPUNITS.ACTIVITY'
  model['LEFT_OPERAND2']            = 'SHIPMENT.DEST.REGION'
  model['CHARGE_ACTION']            = 'A'
  model['CHARGE_TYPE']              = 'B'
  model['LOW_VALUE1']               = 'D'
  model['DOMAIN_NAME']              = 'SUZANO'
  model['OPER1_GID']                = 'EQ'
  model['OPER2_GID']                = 'EQ'
  model['COST_TYPE']                = 'C'
  model['AND_OR1']                  = 'A'

  rate_geo_cost_ton = pd.concat([df_rgct, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)
  rate_geo_cost_ton = rate_geo_cost_ton[~rate_geo_cost_ton['RATE_GEO_COST_GROUP_GID'].isna()]
  rate_geo_cost_ton = rate_geo_cost_ton.to_csv(index=False)
  return rate_geo_cost_ton

def rate_geo_cost_viagem(model, unity):
  model = model.rename(columns={'FRETE': 'CHARGE_AMOUNT'})

  #### Create rate_geo_cost Dataframe ####

  columns_rgcv = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID', 'LEFT_OPERAND1', 'LOW_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_ACTION', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'IS_FILED_AS_TARIFF', 'COST_TYPE', 'ALLOW_ZERO_RBI_VALUE', 'OPERAND_QUALIFIER3', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'DOMAIN_NAME']
  df_rgcv  = pd.DataFrame(columns=columns_rgcv)
  new_row  = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS'"] + [np.nan] * (len(df_rgcv.columns) - 1)], columns=df_rgcv.columns)
  df_rgcv  = pd.concat([new_row, df_rgcv], ignore_index=True)

  #### Building a model to concat with rate_geo_cost (df_rgcv) ####

  from datetime import datetime, timedelta

  current_date = datetime.now()
  one_day_ago  = current_date - timedelta(days=1)
  format_date  = one_day_ago.strftime('%Y%m%d') + '030000'

  if unity == 'UNPE':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
  if unity == 'UNBC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  if unity == 'UNC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  model['EFFECTIVE_DATE']          = format_date
  model['CHARGE_AMOUNT']           = model['CHARGE_AMOUNT'].round(2)
  model['LOW_VALUE2']              = model['DESTINO'].apply(lambda x: f'SUZANO.{x}')

  model['CHARGE_MULTIPLIER_OPTION'] = 'A'
  model['ALLOW_ZERO_RBI_VALUE']     = 'N'
  model['CHARGE_CURRENCY_GID']      = 'BRL'
  model['IS_FILED_AS_TARIFF']       = 'N'
  model['CHARGE_UNIT_COUNT']        = '1'
  model['CHARGE_MULTIPLIER']        = 'SHIPMENT'
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

  rate_geo_cost_viagem = pd.concat([df_rgcv, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)
  rate_geo_cost_viagem = rate_geo_cost_viagem[~rate_geo_cost_viagem['RATE_GEO_COST_GROUP_GID'].isna()]
  rate_geo_cost_viagem = rate_geo_cost_viagem.to_csv(index=False)
  return rate_geo_cost_viagem