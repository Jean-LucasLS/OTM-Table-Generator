import pandas as pd

from otm_core.dicts import origens
from ui.sample_data import get_template_model_df

OTM_DESCRICOES = {
  'FAB_MUC_2100': 'MUCURI',
  'AMZ_CAM_5400': 'CAMPINAS',
  'AMZ_AMA_5400': 'AMERICANA',
  'FAB_LIM_5400': 'LIMEIRA',
  'AMZ_DCO_1101': 'ARUJA',
  'AMZ_PNS_1101': 'ITAPEVI',
  'AMZ_SZ1_1101': 'SUZANLOG 2',
  'AMZ_SZL_1101': 'SUZANLOG',
  'AMZ_DTR_1101': 'GUARULHOS',
  'AMZ_DIN_1101': 'GUARULHOS',
  'FAB_SUZ_1101': 'SUZANO',
  'FAB_RVD_1102': 'RIO VERDE (SUZANO)',
  'CDR_SUZ_1062': 'CD SUZANO',
  'CDL_SUZ_1112': 'CD SUZANO',
  'CDL_CAR_1063': 'CD CARIACICA',
  'FAB_CIT_1064': 'CACHOEIRO DE ITAPEMIRIM',
  'FAB_MOG_1110': 'MOGI DAS CRUZES',
  'CDL_ARU_1111': 'CD ARUJA',
  'FAB_IMP_1301': 'IMPERATRIZ',
  'CDL_MAR_2280': 'CD MARACANAU',
  'FAB_BEL_2283': 'BELEM',
  'FAB_RIB_2298': 'RIBAS DO RIO PARDO',
  'FAB_JAC_6100': 'JACAREI',
  'FAB_ARA_6300': 'ARACRUZ',
  'FAB_TLS_6800': 'TRES LAGOAS',
  'CDL_BHT_1005': 'CD BELO HORIZONTE',
}


def get_documentation_examples():
  model = get_template_model_df()
  model2 = pd.DataFrame({'📍 ORIGEM': ['FAB_SUZ_1101', 'FAB_SUZ_1101']})
  model3 = pd.DataFrame({
    '📍 ORIGEM': ['FSCB', 'FSCB', 'DSUZ', 'DSUZ'],
    '🎯 DESTINO': ['L111111111', 'L999999999', 'L111111111', 'L999999999'],
    '🏷️ SAP': ['444444', '444444', '888888', '888888'],
    '🚚 VEICULO': ['Y06', 'Y06', 'Y12', 'Y12'],
    '💸 FRETE': [22.22, 44.44, 88.88, 16.16],
  })
  model4 = pd.DataFrame({'💾 ID_OTM': ['UN_0000444444_FAB_SUZ_1101_Y06', 'UN_0000888888_AMZ_SZL_1001_Y12']})
  model5 = pd.DataFrame({'📍 ORIGEM': ['FSCB', 'ABDC', 'DSUZ', 'WXYZ']}).rename_axis('Index')
  return model, model2, model3, model4, model5


def get_origens_df():
  sap_otm_pairs = [(sap, otm, OTM_DESCRICOES.get(otm, '')) for sap, otm in origens.items() if sap != otm]
  return pd.DataFrame(sap_otm_pairs, columns=['🏢 SAP', '🏭 OTM', '📝 Descrição'])
