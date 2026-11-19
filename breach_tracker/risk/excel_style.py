"""Apply the professional look to every sheet of the workbook."""
from openpyxl import load_workbook

from .excel_cells import style_body, style_header
from .excel_columns import add_color_scales, fit_widths


def style_excel(output_path: str):
    """Open the saved workbook, style each sheet, save it again."""
    wb = load_workbook(output_path)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        style_header(ws)
        style_body(ws)
        fit_widths(ws)
        ws.freeze_panes = "A2"
        add_color_scales(ws)
    wb.save(output_path)
