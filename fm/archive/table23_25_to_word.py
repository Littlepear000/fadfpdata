import time
import win32com.client as win32
from datetime import datetime

excel_file_path = r"Q:\DATA\FP\Fiscal Monitor\2025-04-April Monitor\MSA\StatTab23-24-25_FMApr2025_20250203.xlsx"

wdPageBreak = 7
wdAlignParagraphLeft = 0
wdGoToPage = 1
wdGoToFirst = 1

def RGB(r, g, b):
    return r + (g << 8) + (b << 16)

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
wb = excel.Workbooks.Open(excel_file_path)

firstSheet = True
ws_count = wb.Worksheets.Count
for i in range(1, ws_count + 1):
    ws = wb.Worksheets(i)
    if ws.Visible:
        ws.Activate()
        if not firstSheet:
            selection.InsertBreak(wdPageBreak)
        else:
            firstSheet = False
        selection.Paragraphs.Alignment = wdAlignParagraphLeft
        selection.Font.Name = "HelveticaNeueLT Com 57 Cn"
        selection.Font.Size = 11
        selection.Font.Color = RGB(112, 48, 160)
        selection.Font.Italic = False
        selection.Font.Bold = True
        b2_text = ws.Range("A1").Value

        selection.TypeText(str(b2_text))
        selection.TypeParagraph()
        selection.Font.Italic = True
        selection.Font.Bold = False
        selection.Paragraphs.Alignment = wdAlignParagraphLeft
        selection.Font.Name = "HelveticaNeueLT Com 57 Cn"
        selection.Font.Size = 10
        selection.Font.Color = RGB(112, 48, 160)
        b3_text = ws.Range("A2").Value
        selection.TypeText(str(b3_text))
        selection.TypeParagraph()
        ws.Range("A3:N62").CopyPicture(Appearance=1, Format=-4147)
        time.sleep(1)
        selection.Paste()

selection.GoTo(What=wdGoToPage, Which=wdGoToFirst)
timestamp = datetime.now().strftime("%Y%m%d %H-%M-%S")
filepath = f"Q:\\DATA\\FP\\Fiscal Monitor\\2025-04-April Monitor\\MSA\\Table23-25_{timestamp}.docx"
wordApp.ActiveDocument.SaveAs2(filepath)
