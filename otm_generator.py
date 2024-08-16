import pandas as pd
import numpy as np
from dicts import origens, veiculos_unbc
from sat_funcs import not_mapped_check, build_model_rg, build_model_rgcg, min_cost_calculation, rate_geo_cost_cols, multicoleta

def rate_geo(model, unity):
  #### Not-mapped origins verifying ####
  not_mapped = not_mapped_check(model)

  #### Create rate_geo Dataframe ####
  columns_rg = ['RATE_GEO_GID', 'RATE_GEO_XID', 'RATE_OFFERING_GID', 'X_LANE_GID', 'EQUIPMENT_GROUP_PROFILE_GID', 'RATE_SERVICE_GID', 'MIN_COST', 'MIN_COST_GID', 'MIN_COST_BASE', 'TOTAL_STOPS_CONSTRAINT', 'PICKUP_STOPS_CONSTRAINT', 'DELIVERY_STOPS_CONSTRAINT', 'CIRCUITY_ALLOWANCE_PERCENT', 'CIRCUITY_DISTANCE_COST', 'CIRCUITY_DISTANCE_COST_GID', 'CIRCUITY_DISTANCE_COST_BASE', 'MAX_CIRCUITY_PERCENT', 'MAX_CIRCUITY_DISTANCE', 'MAX_CIRCUITY_DISTANCE_UOM_CODE', 'MAX_CIRCUITY_DISTANCE_BASE', 'STOPS_INCLUDED_RATE', 'FLEX_COMMODITY_PROFILE_GID', 'RATE_QUALITY_GID', 'SHIPPER_MIN_VALUE', 'MIN_STOPS', 'SHORT_LINE_COST', 'SHORT_LINE_COST_GID', 'SHORT_LINE_COST_BASE', 'RATE_ZONE_PROFILE_GID', 'LOCATION_GID', 'ROUTE_CODE_GID', 'DIM_RATE_FACTOR_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'ALLOW_UNCOSTED_LINE_ITEMS', 'SHIPPER_MIN_VALUE_GID', 'MULTI_BASE_GROUPS_RULE', 'RAIL_INTER_MODAL_PLAN_GID', 'CUSTOMER_RATE_CODE', 'COFC_TOFC', 'EXPIRE_MARK_ID', 'VIA_SRC_LOC_PROF_GID', 'VIA_DEST_LOC_PROF_GID', 'VIA_SRC_LOC_GID', 'VIA_DEST_LOC_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'BUY_SERVPROV_PROFILE_GID', 'BUY_RATE_GEO_PROFILE_GID', 'PAYMENT_METHOD_CODE_GID', 'IS_MASTER_OVERRIDES_BASE', 'HAZARDOUS_RATE_TYPE', 'IS_QUOTE', 'DOMAIN_PROFILE_GID', 'RO_TIME_PERIOD_DEF_GID', 'LOGIC_CONFIG_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE6', 'ATTRIBUTE7', 'ATTRIBUTE8', 'ATTRIBUTE9', 'ATTRIBUTE11', 'ATTRIBUTE12', 'ATTRIBUTE13', 'ATTRIBUTE14', 'ATTRIBUTE15', 'ATTRIBUTE16', 'ATTRIBUTE17', 'ATTRIBUTE18', 'ATTRIBUTE19', 'ATTRIBUTE20', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER5', 'ATTRIBUTE_NUMBER6', 'ATTRIBUTE_NUMBER7', 'ATTRIBUTE_NUMBER8', 'ATTRIBUTE_NUMBER9', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ATTRIBUTE_DATE6', 'ATTRIBUTE_DATE7', 'ATTRIBUTE_DATE8', 'ATTRIBUTE_DATE9', 'ATTRIBUTE_DATE10', 'RATE_GEO_DESC', 'IS_FOR_BEYOND', 'IS_FROM_BEYOND', 'CORPORATION_PROFILE_GID', 'PARENT_RATE_GEO_GID', 'IS_SOURCING_RATE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'DOMAIN_NAME']
  new_row    = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'"] + [np.nan] * (len(columns_rg) - 1)], columns=columns_rg)
  df_rg      = pd.concat([new_row, pd.DataFrame(columns=columns_rg)], ignore_index=True)
  
  ## Building a model to concat with rate_geo (df_rg) ##
  model    = model.drop_duplicates(subset=['ORIGEM', 'SAP', 'VEICULO'], keep='first')
  model    = build_model_rg(model, unity)
  rate_geo = pd.concat([df_rg, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO', 'FRETE'])], ignore_index=True)

  #### Creating rate_geo_cost_group (df_rgcg) based on rate_geo ####
  df_rgcg, modelcg = build_model_rgcg(model)

  if unity == 'UNPE':
    modelcg['MULTI_RATES_RULE'] = np.where(modelcg['RATE_GEO_COST_GROUP_XID'].str[:9] == 'UNPE_MULT', 'A', 'X')

  rate_geo_cost_group = pd.concat([df_rgcg, modelcg], ignore_index=True)

  rate_geo_csv            = rate_geo.to_csv(index=False)
  rate_geo_cost_group_csv = rate_geo_cost_group.to_csv(index=False)
  return rate_geo_csv, rate_geo_cost_group_csv, not_mapped

def rate_geo_cost_ton(model, unity, min_cost=True):
  model = model.rename(columns={'FRETE': 'CHARGE_AMOUNT'})

  ## Create rate_geo_cost Dataframe ##
  columns_rgct = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID', 'LEFT_OPERAND1', 'LOW_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_ACTION', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'IS_FILED_AS_TARIFF', 'COST_TYPE', 'ALLOW_ZERO_RBI_VALUE', 'OPERAND_QUALIFIER3', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'DOMAIN_NAME']
  new_row      = pd.DataFrame([["EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS'"] + [np.nan] * (len(columns_rgct) - 1)], columns=columns_rgct)
  df_rgct      = pd.concat([new_row, pd.DataFrame(columns=columns_rgct)], ignore_index=True)
  df_mults     = False # If unity != UNPE, df_mults will return False

  ## Building a model to concat with rate_geo_cost (df_rgct) ##
  model = rate_geo_cost_cols(model)
  model['CHARGE_UNIT_UOM_CODE'] = 'MTON'
  model['CHARGE_MULTIPLIER']    = 'SHIPMENT.WEIGHT'

  if min_cost:
    model = min_cost_calculation(model, unity)

  if unity == 'UNPE':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
    df_mults                         = multicoleta(model)
    df_mults                         = df_mults.to_csv(index=False)
  if unity == 'UNBC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  if unity == 'UNC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  rate_geo_cost_ton = pd.concat([df_rgct, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)
  rate_geo_cost_ton = rate_geo_cost_ton[~rate_geo_cost_ton['RATE_GEO_COST_GROUP_GID'].isna()]

  rate_geo_cost_ton = rate_geo_cost_ton.to_csv(index=False)
  return rate_geo_cost_ton, df_mults

def rate_geo_cost_viagem(model, unity):
  model = model.rename(columns={'FRETE': 'CHARGE_AMOUNT'})

  ## Create rate_geo_cost Dataframe ##
  columns_rgcv  = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID', 'LEFT_OPERAND1', 'LOW_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_ACTION', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'IS_FILED_AS_TARIFF', 'COST_TYPE', 'ALLOW_ZERO_RBI_VALUE', 'OPERAND_QUALIFIER3', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'DOMAIN_NAME']
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

  model = rate_geo_cost_cols(model)
  model['CHARGE_MULTIPLIER'] = 'SHIPMENT'

  rate_geo_cost_viagem = pd.concat([df_rgcv, model.drop(columns=['ORIGEM', 'DESTINO', 'SAP', 'VEICULO'])], ignore_index=True)
  rate_geo_cost_viagem = rate_geo_cost_viagem[~rate_geo_cost_viagem['RATE_GEO_COST_GROUP_GID'].isna()]
  rate_geo_cost_viagem = rate_geo_cost_viagem.to_csv(index=False)
  return rate_geo_cost_viagem