import pandas as pd
import numpy as np
from otm_core.dicts import origens, veiculos_unbc
from otm_core.calculations import min_cost_calculation, direct_mult_split_ton
from otm_core.multicoleta import multicoleta
from otm_core.column_builders import not_mapped_check, build_model_rg, build_model_rgcg, rate_geo_cost_cols, df_rgcv_cols

DROP_INPUT_COLUMNS = ['ORIGEM', 'DESTINO', 'SAP', 'VEICULO']
COLUMNS_RGCT = ['RATE_GEO_COST_GROUP_GID', 'OPER1_GID' ,'LEFT_OPERAND1', 'LOW_VALUE1', 'HIGH_VALUE1', 'AND_OR1', 'OPER2_GID', 'LEFT_OPERAND2', 'LOW_VALUE2', 'HIGH_VALUE2', 'AND_OR2', 'OPER3_GID', 'LEFT_OPERAND3', 'LOW_VALUE3', 'HIGH_VALUE3', 'AND_OR3', 'OPER4_GID', 'LEFT_OPERAND4', 'LOW_VALUE4', 'HIGH_VALUE4', 'CHARGE_AMOUNT', 'CHARGE_CURRENCY_GID', 'CHARGE_AMOUNT_BASE', 'CHARGE_UNIT_UOM_CODE', 'CHARGE_UNIT_COUNT', 'CHARGE_MULTIPLIER', 'CHARGE_MULTIPLIER_SCALAR', 'CHARGE_ACTION', 'CHARGE_BREAK_COMPARATOR', 'CHARGE_TYPE', 'CHARGE_MULTIPLIER_OPTION', 'CHARGE_MULTIPLIER2', 'CHARGE_UNIT_COUNT2', 'CHARGE_UNIT_UOM_CODE2', 'CHARGE_SEQUENCE', 'DIM_RATE_FACTOR_GID', 'ROUNDING_TYPE', 'ROUNDING_INTERVAL', 'ROUNDING_FIELDS_LEVEL', 'ROUNDING_APPLICATION', 'DEFICIT_CALCULATIONS_TYPE', 'MIN_COST', 'MIN_COST_CURRENCY_GID', 'MIN_COST_BASE', 'MAX_COST', 'MAX_COST_CURRENCY_GID', 'MAX_COST_BASE', 'PAYMENT_METHOD_CODE_GID', 'EFFECTIVE_DATE', 'EXPIRATION_DATE', 'CALENDAR_GID', 'IS_FILED_AS_TARIFF', 'TIER', 'COST_TYPE', 'CALENDAR_ACTIVITY_GID', 'RATE_UNIT_BREAK_PROFILE_GID', 'RATE_UNIT_BREAK_PROFILE2_GID', 'CHARGE_BREAK_COMPARATOR2_GID', 'EXTERNAL_RATING_ENGINE_GID', 'EXT_RE_FIELDSET_GID', 'COST_CODE_GID', 'LOGIC_PARAM_QUAL_GID', 'COST_CATEGORY_GID', 'ATTRIBUTE1', 'ATTRIBUTE2', 'ATTRIBUTE3', 'ATTRIBUTE4', 'ATTRIBUTE5', 'ATTRIBUTE_NUMBER1', 'ATTRIBUTE_NUMBER2', 'ATTRIBUTE_NUMBER3', 'ATTRIBUTE_NUMBER4', 'ATTRIBUTE_NUMBER10', 'ATTRIBUTE_DATE1', 'ATTRIBUTE_DATE2', 'ATTRIBUTE_DATE3', 'ATTRIBUTE_DATE4', 'ATTRIBUTE_DATE5', 'ALLOW_ZERO_RBI_VALUE', 'CALC_CHARGEABLE_WT_VOL_WITH', 'OPERAND_QUALIFIER1', 'OPERAND_QUALIFIER2', 'OPERAND_QUALIFIER3', 'OPERAND_QUALIFIER4', 'CHARGE_QUALIFIER1', 'CHARGE_QUALIFIER2', 'CHARGE_BREAK_COMP_QUALIFIER1', 'CHARGE_BREAK_COMP_QUALIFIER2', 'DOMAIN_NAME']


def _build_sql_header_frame(columns, sql_header):
  new_row = pd.DataFrame([[sql_header] + [np.nan] * (len(columns) - 1)], columns=columns)
  return pd.concat([new_row, pd.DataFrame(columns=columns)], ignore_index=True)


def _apply_unbc_opl_prefix(df, columns):
  for col in columns:
    if col in df.columns:
      df[col] = df[col].str.replace('UNBC_', 'UNBC_OPL_', regex=False)
  return df


def rate_geo(model, unity, mult_flag=False, opl_flag=False):
  not_mapped          = not_mapped_check(model) # Not-mapped origins verifying
  rate_geo, model     = build_model_rg(model, unity, mult_flag)
  rate_geo_cost_group = build_model_rgcg(model, unity, mult_flag)

  if unity == 'UNBC' and opl_flag:
    rate_geo = _apply_unbc_opl_prefix(rate_geo, ['RATE_GEO_GID', 'RATE_GEO_XID', 'RATE_OFFERING_GID'])
    rate_geo_cost_group = _apply_unbc_opl_prefix(rate_geo_cost_group, ['RATE_GEO_COST_GROUP_GID', 'RATE_GEO_COST_GROUP_XID', 'RATE_GEO_GID'])

  return rate_geo.to_csv(index=False), rate_geo_cost_group.to_csv(index=False), not_mapped

def rate_geo_cost_ton(model, unity, min_cost=True, mult_flag=False, opl_flag=False):
  df_rgct = _build_sql_header_frame(COLUMNS_RGCT, "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS'")

  ## Create df_rgct Dataframe and building a model to concat with rate_geo_cost_ton ##
  model                         = rate_geo_cost_cols(model)
  model['CHARGE_UNIT_UOM_CODE'] = 'MTON'
  model['CHARGE_MULTIPLIER']    = 'SHIPMENT.WEIGHT'

  if min_cost:
    model = min_cost_calculation(model, unity)

  if unity == 'UNPE':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO']
    model                            = multicoleta(model)
  if unity == 'UNBC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens) + '_' + model['VEICULO'].map(veiculos_unbc)
  if unity == 'UNC':
    model['RATE_GEO_COST_GROUP_GID'] = f'SUZANO.{unity}_0000' + model['SAP'].astype(str) + '_' + model['ORIGEM'].map(origens)

  if unity == 'UNPE':
    model = direct_mult_split_ton(model, mult_flag)

  rate_geo_cost_ton = pd.concat([df_rgct, model.drop(columns=DROP_INPUT_COLUMNS)], ignore_index=True)
  rate_geo_cost_ton = rate_geo_cost_ton[~rate_geo_cost_ton['RATE_GEO_COST_GROUP_GID'].isna()]

  return rate_geo_cost_ton.to_csv(index=False)

def rate_geo_cost_viagem(model, unity, opl_flag=False):
  rate_geo_cost_viagem = df_rgcv_cols(model, unity)
  if unity == 'UNBC' and opl_flag:
    rate_geo_cost_viagem = _apply_unbc_opl_prefix(rate_geo_cost_viagem, ['RATE_GEO_COST_GROUP_GID'])
  return rate_geo_cost_viagem.to_csv(index=False)
