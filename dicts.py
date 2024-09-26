origens = {'FBMU': 'FAB_MUC_2100', 'FAB_MUC_2100': 'FAB_MUC_2100', # MUC
  ## LIM ## 
  'DCAM': 'AMZ_CAM_5400', 'AMZ_CAM_5400': 'AMZ_CAM_5400',
  'DMBM': 'AMZ_AME_5400', 'AMZ_AME_5400': 'AMZ_AME_5400',
  'FRPL': 'FAB_LIM_5400', 'FAB_LIM_5400': 'FAB_LIM_5400',
  'AMZ_DRT_5400': 'AMZ_DRT_5400', # 'DTRI': 'AMZ_DRT_5400',
  ## SUZ ##
  'DCOP': 'AMZ_DCO_1101', 'AMZ_DCO_1101': 'AMZ_DCO_1101',
  'DPNS': 'AMZ_PNS_1101', 'AMZ_PNS_1101': 'AMZ_PNS_1101',
  'DSU1': 'AMZ_SZ1_1101', 'AMZ_SZ1_1101': 'AMZ_SZ1_1101',
  'DSUZ': 'AMZ_SZL_1101', 'AMZ_SZL_1101': 'AMZ_SZL_1101',
  'DTRI': 'AMZ_DTR_1101', 'AMZ_DTR_1101': 'AMZ_DTR_1101',
  'FSCB': 'FAB_SUZ_1101', 'FAB_SUZ_1101': 'FAB_SUZ_1101',
  'FSCC': 'FAB_RVD_1102', 'FAB_RVD_1102': 'FAB_RVD_1102',
  'CDRZ': 'CDR_SUZ_1062', 'CDR_SUZ_1062': 'CDR_SUZ_1062',
  'SSUZ': 'CDL_SUZ_1112', 'CDL_SUZ_1112': 'CDL_SUZ_1112',
  ## Outros ##
  'SVIA': 'CDL_CAR_1063', 'CDL_CAR_1063': 'CDL_CAR_1063',
  'FCIT': 'FAB_CIT_1064', 'FAB_CIT_1064': 'FAB_CIT_1064',
  'FBMA': 'FAB_IMP_1301', 'FAB_IMP_1301': 'FAB_IMP_1301',
  'SMAR': 'CDL_MAR_2280', 'CDL_MAR_2280': 'CDL_MAR_2280',
  'FCBL': 'FAB_BEL_2283', 'FAB_BEL_2283': 'FAB_BEL_2283',
  'FBRP': 'FAB_RIB_2298', 'FAB_RIB_2298': 'FAB_RIB_2298',
  'FJAC': 'FAB_JAC_6100', 'FAB_JAC_6100': 'FAB_JAC_6100',
  'FARA': 'FAB_ARA_6300', 'FAB_ARA_6300': 'FAB_ARA_6300',
  'FTLS': 'FAB_TLS_6800', 'FAB_TLS_6800': 'FAB_TLS_6800',
  ## CDs ##
  'SBHZ': 'CDL_BHT_1005',
  }

origens_mult = {
  ## LIM ##
  'DCAM': 'AMZ_CAM_5400', 'AMZ_CAM_5400': 'AMZ_CAM_5400',
  'DMBM': 'AMZ_AME_5400', 'AMZ_AME_5400': 'AMZ_AME_5400',
  'FRPL': 'FAB_LIM_5400', 'FAB_LIM_5400': 'FAB_LIM_5400',
  ## SUZ ##
  'DCOP': 'AMZ_DCO_1101', 'AMZ_DCO_1101': 'AMZ_DCO_1101',
  'DPNS': 'AMZ_PNS_1101', 'AMZ_PNS_1101': 'AMZ_PNS_1101',
  'DSU1': 'AMZ_SZ1_1101', 'AMZ_SZ1_1101': 'AMZ_SZ1_1101',
  'DSUZ': 'AMZ_SZL_1101', 'AMZ_SZL_1101': 'AMZ_SZL_1101',
  'DTRI': 'AMZ_DTR_1101', 'AMZ_DTR_1101': 'AMZ_DTR_1101',
  'FSCB': 'FAB_SUZ_1101', 'FAB_SUZ_1101': 'FAB_SUZ_1101',
  'FSCC': 'FAB_RVD_1102', 'FAB_RVD_1102': 'FAB_RVD_1102',
  'CDRZ': 'CDR_SUZ_1062', 'CDR_SUZ_1062': 'CDR_SUZ_1062',
  'SSUZ': 'CDL_SUZ_1112', 'CDL_SUZ_1112': 'CDL_SUZ_1112',}

equipms_unpe = {'Y02': 'SUZANO.Y02_TRUCK_UNPE',
  'Y06': 'SUZANO.Y06_CARRETA_UNPE', 'Y12': 'SUZANO.Y12_VANDERLEIA_UNPE',
  'Y17': 'SUZANO.Y17_CARRETA_BITREM_UNPE', 'Y23': 'SUZANO.Y23_CAR_RODO_UNPE'}

equipms_unbc = {
  'Y02': 'SUZANO.Y02_TRUCK_UNBC',
  'Y06': 'SUZANO.Y06_CARRETA_UNBC', 'Y12': 'SUZANO.Y12_CARRETA_UNBC',
  'Y17': 'SUZANO.Y17_CARRETA_BI_UNBC', 'Y23': 'SUZANO.Y23_CARRETA_BI_UNBC'
}

veiculos_unbc = {
  'Y02': 'TRUCK', 'Y06': 'CARRETA', 'Y12': 'CARRETA', 'Y17': 'CARRETA_BI', 'Y23': 'CARRETA_BI',
  'TRUCK': 'TRUCK', 'CARRETA': 'CARRETA', 'CARRETA_BI': 'CARRETA_BI'
}

min_ton = {'Y02': 12.5, 'Y06': 25, 'Y12': 25, 'Y17': 36, 'Y23': 45}