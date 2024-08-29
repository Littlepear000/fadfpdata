from fadfpdata.fm import *

health_raw = pd.read_excel(fr'{input_folder}\Health and Pension Projections_20240823.xlsx', sheet_name='health_fm')
pension_raw = pd.read_excel(fr'{input_folder}\Health and Pension Projections_20240823.xlsx', sheet_name='pension_fm')

health = health_raw[['ifscode', 'Y_2023_to_2030', 'NPV2023_2050_health']].rename(columns={
    'Y_2023_to_2030': 'Y_2023_to_2030_health'
})
pension = pension_raw[['ifscode', 'Y_2023_to_2030', 'NPV2023_2050_pension']].rename(columns={
    'Y_2023_to_2030': 'Y_2023_to_2030_pension'
})

ep = pension.merge(health, on='ifscode', how='outer')