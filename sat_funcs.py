import pandas as pd

from dicts import origens_suz, origens, equipms_unpe, equipms_unbc, veiculos_unbc

def not_mapped_check(model):
  not_mapped               = model.copy()
  not_mapped['NOT_MAPPED'] = not_mapped['ORIGEM'].map(origens)
  not_mapped               = not_mapped[not_mapped['NOT_MAPPED'].isna()]
  not_mapped               = not_mapped.rename_axis('Index')
  not_mapped               = not_mapped['ORIGEM']
  return not_mapped

def suz_mult(model):
  mult = model.copy()
  mult = mult[mult['X_LANE_GID'].str.replace('SUZANO.', '').str.replace('_BRA', '').isin(origens_suz)]

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