"""Colours, fonts and borders for the Excel workbook."""
from openpyxl.styles import Border, Font, PatternFill, Side

HEADER_FILL = PatternFill("solid", fgColor="1F2937")  # dark slate
HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
ALT_FILL = PatternFill("solid", fgColor="F9FAFB")
_SIDE = Side(style="thin", color="E5E7EB")
CELL_BORDER = Border(left=_SIDE, right=_SIDE, top=_SIDE, bottom=_SIDE)
