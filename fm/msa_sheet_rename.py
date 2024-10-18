import xlwings as xw

# 定义文件路径
file_path = r'Q:\DATA\FP\Fiscal Monitor\2024-10-October_Monitor\MSA\MSA_database_20241017.xlsx'

# 使用xlwings打开工作簿
wb = xw.Book(file_path)

# 遍历所有工作表
for sheet in wb.sheets:
    # 替换工作表名称中的 'STAT' 为 'Table A'
    new_name = sheet.name.replace('STAT', 'Table A')
    sheet.name = new_name  # 修改工作表名称

# 保存并关闭工作簿
wb.save()
wb.close()