import re
import argparse
import sys
from pathlib import Path
import win32com.client as win32

# Word constants we'll use
from win32com.client import constants as wd

def mark_headings(doc):
    """
    Find paragraphs whose text starts with 'Table ' and mark them as Heading 1.
    Return the count of headings marked.
    """
    count = 0
    paragraphs = doc.Paragraphs
    for i in range(1, paragraphs.Count + 1):
        p = paragraphs(i)
        text = p.Range.Text.strip()
        if text.startswith("Table "):
            try:
                p.Range.Style = "Heading 1"
                count += 1
            except Exception:
                # Fallback to constant if style string not found
                try:
                    p.Range.Style = wd.wdStyleHeading1
                    count += 1
                except Exception:
                    pass
    return count

def ensure_toc_at_top(doc):
    """
    Insert "Table of Contents" at the very top, create a bookmark "ToC",
    insert the Word ToC right beneath it (hyperlinked, no page numbers),
    and add a page break after the ToC.
    """
    # Insert title and two newlines at absolute start
    title = "Table of Contents"
    # Range(0,0) is absolute start of document
    top = doc.Range(0, 0)
    top.InsertBefore(title + "\r\r")

    # Style the first paragraph as Title
    try:
        doc.Paragraphs(1).Range.Style = "Title"
    except Exception:
        pass  # non-critical

    # Bookmark the title text as "ToC"
    # The title is the very first paragraph we just inserted
    title_range = doc.Paragraphs(1).Range
    # Bookmark on the *title paragraph* (not the blank line)
    try:
        # If bookmark exists, delete to avoid duplicate
        if doc.Bookmarks.Exists("ToC"):
            doc.Bookmarks("ToC").Delete()
    except Exception:
        pass
    doc.Bookmarks.Add("ToC", title_range)

    # Insert the ToC field at paragraph 2 (the blank line under the title)
    toc_anchor = doc.Paragraphs(2).Range
    # Word may throw if a ToC exists already—remove all existing ToCs
    try:
        for idx in range(doc.TablesOfContents.Count, 0, -1):
            doc.TablesOfContents(idx).Delete()
    except Exception:
        pass

    # Add a new hyperlinked ToC, using Heading 1 only, without page numbers
    toc = doc.TablesOfContents.Add(
        Range=toc_anchor,
        UseHeadingStyles=True,
        UpperHeadingLevel=1,
        LowerHeadingLevel=1,
        RightAlignPageNumbers=False,
        IncludePageNumbers=False,
        UseHyperlinks=True
    )
    # Update the ToC so entries appear immediately
    toc.Update()

    # Add a page break *after* the ToC paragraph
    # The ToC occupies paragraph 2; insert break after it.
    try:
        after_toc = doc.Paragraphs(2).Range
        after_toc.Collapse(wd.wdCollapseEnd)
        after_toc.InsertBreak(wd.wdPageBreak)
    except Exception:
        # Fallback: insert a page break at document start if above fails
        doc.Range(0, 0).InsertBreak(wd.wdPageBreak)

def add_return_links_after_tables(doc):
    """
    After each table, insert a "Return to ToC" hyperlink pointing to the ToC bookmark.
    Avoid duplicating if the same link text already exists immediately after the table.
    """
    link_text = "Return to ToC"

    # Iterate over a *copy* of Tables collection by index because it is live
    table_count = doc.Tables.Count
    for i in range(1, table_count + 1):
        table = doc.Tables(i)
        rng = table.Range.Duplicate
        end_before = rng.End

        # Insert a new paragraph with our link text
        rng.Collapse(wd.wdCollapseEnd)
        rng.InsertAfter("\r" + link_text + "\r")

        # The inserted text starts at end_before + 1 (skipping the first CR)
        start = end_before + 1
        end = start + len(link_text)
        link_range = doc.Range(start, end)

        # If there is already a hyperlink on this exact range, skip adding
        already_linked = False
        try:
            for h in doc.Hyperlinks:
                if h.Range.Start == link_range.Start and h.Range.End == link_range.End:
                    already_linked = True
                    break
        except Exception:
            pass

        if not already_linked:
            # Create a subaddress (bookmark) hyperlink to "ToC"
            doc.Hyperlinks.Add(Anchor=link_range, Address="", SubAddress="ToC", TextToDisplay=link_text)

def process(input_path, output_path):
    word = None
    doc = None
    try:
        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Visible = False  # set True for debugging / visual mode

        doc = word.Documents.Open(str(input_path))

        # 1) Mark headings so ToC can be built
        marked = mark_headings(doc)

        # 2) Insert ToC at top (title, bookmark, ToC field, page break)
        ensure_toc_at_top(doc)

        # 3) Insert "Return to ToC" after each table
        add_return_links_after_tables(doc)

        # Save to output
        doc.SaveAs(str(output_path))
        print(f"Done. Headings marked: {marked}. Saved to: {output_path}")
    finally:
        try:
            if doc is not None:
                doc.Close(SaveChanges=False)
        except Exception:
            pass
        try:
            if word is not None:
                word.Quit()
        except Exception:
            pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True, help="Path to input .docx")
    ap.add_argument("--output", "-o", required=False, help="Path to output .docx (default: add _with_links)")
    args = ap.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        print(f"Input not found: {in_path}")
        sys.exit(1)

    out_path = Path(args.output).expanduser().resolve() if args.output else in_path.with_name(in_path.stem + "_with_links.docx")

    process(in_path, out_path)

if __name__ == "__main__":
    main()