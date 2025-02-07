import time
import win32com.client as win32
from datetime import datetime

table1_22_excel = r"Q:\DATA\FP\Fiscal Monitor\2025-04-April Monitor\MSA\Stat_Tables1-22_FMApr2025.xlsm"
table23_25_excel = r"Q:\DATA\FP\Fiscal Monitor\2025-04-April Monitor\MSA\StatTab23-24-25_FMApr2025_20250203.xlsx"

wdPageBreak = 7
wdAlignParagraphLeft = 0
wdGoToPage = 1
wdGoToFirst = 1

def RGB(r, g, b):
    return r + (g << 8) + (b << 16)

def set_title_format(
        font_size: int,
        bold: bool,
        italic: bool
):
    selection.Paragraphs.Alignment = wdAlignParagraphLeft
    selection.Font.Name = "HelveticaNeueLT Com 57 Cn"
    selection.Font.Color = RGB(112, 48, 160)
    selection.Font.Size = font_size
    selection.Font.Italic = italic
    selection.Font.Bold = bold

def export_table2word(
        title_cell: str,
        subtiltel_cell: str,
        table_range: str
):
    set_title_format(font_size=11, bold=True, italic=False)
    b2_text = ws.Range(title_cell).Value

    selection.TypeText(str(b2_text))
    selection.TypeParagraph()
    set_title_format(font_size=10, bold=False, italic=True)
    b3_text = ws.Range(subtiltel_cell).Value
    selection.TypeText(str(b3_text))
    selection.TypeParagraph()
    ws.Range(table_range).CopyPicture(Appearance=1, Format=-4147)
    time.sleep(1)
    selection.Paste()

wordApp = win32.Dispatch("Word.Application")
wordApp.Visible = True
wordApp.Activate()
wordApp.Documents.Add()
selection = wordApp.Selection

paraFormat = selection.ParagraphFormat
paraFormat.SpaceBefore = 0
paraFormat.SpaceBeforeAuto = False
paraFormat.SpaceAfter = 0
paraFormat.SpaceAfterAuto = False
paraFormat.LineSpacing = 13.2

excel = win32.Dispatch("Excel.Application")
excel.Visible = True

# export table 1-22
wb = excel.Workbooks.Open(table1_22_excel)
firstSheet = True
ws_count = wb.Worksheets.Count
for i in range(7, ws_count + 1):
    ws = wb.Worksheets(i)
    if ws.Visible:
        ws.Activate()
        if not firstSheet:
            selection.InsertBreak(wdPageBreak)
        else:
            firstSheet = False
        export_table2word(title_cell='B2', subtiltel_cell='B3', table_range='B4:R62')

# export table 23-25
wb = excel.Workbooks.Open(table23_25_excel)
ws_count = wb.Worksheets.Count
for i in range(1, ws_count + 1):
    ws = wb.Worksheets(i)
    if ws.Visible:
        ws.Activate()
        selection.InsertBreak(wdPageBreak)
        export_table2word(title_cell='A1', subtiltel_cell='A2', table_range='A3:N62')

selection.GoTo(What=wdGoToPage, Which=wdGoToFirst)
timestamp = datetime.now().strftime("%Y%m%d %H-%M-%S")
filepath = f"Q:\\DATA\\FP\\Fiscal Monitor\\2025-04-April Monitor\\MSA\\Table1-25_{timestamp}.docx"
wordApp.ActiveDocument.SaveAs2(filepath)
