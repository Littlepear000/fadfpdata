import xlwings as xw

def test(file_path):

    wb = xw.Book(file_path)
    wb.app.visible = True

    # 遍历所有工作表
    for sheet in wb.sheets:
        start_cell = sheet.range("D6")
        last_cell = sheet.range("D100").end('up').end('right')  # 找到最后一个有内容的单元格

        # 根据起始单元格和结束单元格定义有效范围
        table_range = sheet.range(start_cell, last_cell)

        # 复制从 D6 开始的表格区域
        table_range.api.Copy()

        # 粘贴到 D6，并将粘贴选项设置为仅保留值 (-4163 = xlPasteValues)
        sheet.range("D6").api.PasteSpecial(Paste=-4163)
    wb.save()


if __name__ == '__main__':
    test(r'C:\Users\xli7\OneDrive - International Monetary Fund (PRD)\Shelley_My Projects\Fiscal Monitor\202410\MSA\MSA_20241009.xlsx')