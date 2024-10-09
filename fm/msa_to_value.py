import xlwings as xw


table1_22 = r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_My Projects\Fiscal Monitor\202410\MSA\test.xlsm'
wb = xw.Book(table1_22)


def convert_formulas_to_values(output_date):
    wb = xw.Book(table1_22)

    new_file_path = fr'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_My Projects\Fiscal Monitor\202410\MSA\MSA_{output_date}.xlsx'
    wb.save(new_file_path)

    # 重新打开新文件，确保对副本进行操作
    new_wb = xw.Book(new_file_path)

    for sheet in wb.sheets:
        for cell in sheet.used_range:
            if cell.formula:
                cell.value = cell.value

    wb.save()


# def convert_formulas_to_values(file_path):
#     wb = xw.Book(file_path)
#
#     # 遍历所有工作表
#     for sheet in wb.sheets:
#         # 选择整个工作表
#         sheet.api.UsedRange.Copy()  # 复制工作表中使用过的区域
#         sheet.api.UsedRange.PasteSpecial(Paste=-4163)  # 粘贴时仅保留值 (-4163 = xlPasteValues)


if __name__ == '__main__':
    convert_formulas_to_values('20241008')