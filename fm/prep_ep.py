from fadfpdata.fm import *

health_raw = pd.read_excel(fr'{input_folder}\Health and Pension Projections_{ep_update_date}.xlsx', sheet_name='health_fm')
pension_raw = pd.read_excel(fr'{input_folder}\Health and Pension Projections_{ep_update_date}.xlsx', sheet_name='pension_fm')

health = health_raw[['ifscode', f'Y_{ep_start_year}_to_2030', f'NPV{ep_start_year}_2050_health']].rename(columns={
    f'Y_{ep_start_year}_to_2030': f'Y_{ep_start_year}_to_2030_health'
})
pension = pension_raw[['ifscode', f'Y_{ep_start_year}_to_2030', f'NPV{ep_start_year}_2050_pension']].rename(columns={
    f'Y_{ep_start_year}_to_2030': f'Y_{ep_start_year}_to_2030_pension'
})

ep = pension.merge(health, on='ifscode', how='outer')