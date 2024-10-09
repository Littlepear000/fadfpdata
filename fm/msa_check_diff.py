


# 定义文件路径
file_path_old = r'C:\Users\xli7\Desktop\MSA_1004_2.xlsx'
file_path_new = r'Q:\DATA\FP\Fiscal Monitor\2024-10-October_Monitor\MSA\FM_October_2024_Methodological and Statistical Appendix_20241008.xlsx'
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

wb1 = load_workbook(file_path_old)
wb2 = load_workbook(file_path_new)

# Iterate through each sheet and compare
for sheet_name in wb1.sheetnames:
    # Load sheets
    sheet1 = wb1[sheet_name]
    sheet2 = wb2[sheet_name]

    # Iterate through each cell in the range of sheet1 and sheet2
    for row in sheet1.iter_rows(min_row=1, max_row=sheet1.max_row, min_col=1, max_col=sheet1.max_column):
        for cell in row:
            # Get corresponding cell from sheet2
            cell2 = sheet2[cell.coordinate]

            # Compare cells and change font color if not equal
            if cell.value is not None and cell2.value is not None:
                if isinstance(cell.value, (int, float)) and isinstance(cell2.value, (int, float)):
                    if round(cell.value, 1) != round(cell2.value, 1):
                        # 如果两者近似比较不相等，将 cell2 的字体颜色改为红色
                        cell2.font = Font(name='Arial', size=9, color="FF0000")
            else:
                cell2.font = Font(color="000000")
# Save the modified workbook
output_path = r"C:\Users\xli7\Desktop\MSA_1008_modified.xlsx"
wb2.save(output_path)

