"""Header row and body-cell styling for one worksheet."""
from openpyxl.styles import Alignment

from .excel_theme import ALT_FILL, CELL_BORDER, HEADER_FILL, HEADER_FONT


def style_header(ws):
    """Dark, bold, centred first row."""
    for cell in ws[1]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center",
                                   vertical="center", wrap_text=True)
        cell.border = CELL_BORDER


def style_body(ws):
    """Borders on every cell and zebra striping on even rows."""
    for row_idx in range(2, ws.max_row + 1):
        fill = ALT_FILL if row_idx % 2 == 0 else None
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = CELL_BORDER
            if fill:
                cell.fill = fill
            cell.alignment = Alignment(vertical="center")
