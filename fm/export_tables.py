import xlwings as xw
from datetime import datetime
import win32com.client as win32


def copy_paste_tables():
    # Create a new instance of Word
    word_app = win32.gencache.EnsureDispatch('Word.Application')
    word_app.Visible = True
    word_doc = word_app.Documents.Add()

    # Set paragraph formatting
    word_app.Selection.ParagraphFormat.SpaceBefore = 0
    word_app.Selection.ParagraphFormat.SpaceAfter = 0
    word_app.Selection.ParagraphFormat.LineSpacing = 13.2

    # Open the active Excel workbook
    wb = xw.Book.caller()

    # Loop through each worksheet
    for i in range(1, len(wb.sheets)):  # Start from 2nd sheet (index 1)
        ws = wb.sheets[i]
        if ws.visible:
            # Add a new section in Word
            word_doc.Sections.Add()

            # Write titles to Word
            word_app.Selection.BoldRun()
            word_app.Selection.Paragraphs.Alignment = win32.constants.wdAlignParagraphLeft
            word_app.Selection.Font.Name = "HelveticaNeueLT Com 57 Cn"
            word_app.Selection.Font.Size = 11
            # Set font color using bitwise operations
            word_app.Selection.Font.Color = (112 << 16) + (48 << 8) + 160  # RGB(112, 48, 160)

            word_app.Selection.TypeText(ws.range("B2").value)
            word_app.Selection.TypeParagraph()

            word_app.Selection.Font.Italic = True
            word_app.Selection.Font.Bold = False
            word_app.Selection.Font.Size = 10
            word_app.Selection.TypeText(ws.range("B3").value)
            word_app.Selection.TypeParagraph()

            # Copy the specified range as a picture
            ws.range("B4:R62").copy_picture()
            word_app.Selection.Paste()

            # Move to the next page
            # word_app.Selection.GoTo(What=win32.constants.wdGoToPage, Which=win32.constants.wdGoToNext)

    # Save the document
    word_app.Selection.GoTo(What=win32.constants.wdGoToPage, Which=win32.constants.wdGoToFirst)
    file_name = fr"C:\Users\xli7\Desktop\Table1-22_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.docx"
    word_doc.SaveAs2(file_name)

    # Cleanup
    word_doc.Close()
    word_app.Quit()


if __name__ == "__main__":
    xw.Book(r"Q:\DATA\FP\Fiscal Monitor\2024-10-October_Monitor\MSA\Stat_Tables1-22_FMOct2024_20240925.xlsm").set_mock_caller()  # Replace with your workbook name
    copy_paste_tables()
