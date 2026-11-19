"""Column-level formatting: widths, freeze panes, colour scales."""
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter


def fit_widths(ws):
    """Auto-size columns from the first ~200 rows (max width 40)."""
    for col_idx in range(1, ws.max_column + 1):
        max_len = 0
        for row_idx in range(1, min(ws.max_row + 1, 200)):
            val = ws.cell(row=row_idx, column=col_idx).value
            if val:
                max_len = max(max_len, len(str(val)))
        letter = get_column_letter(col_idx)
        ws.column_dimensions[letter].width = min(max_len + 4, 40)


def add_color_scales(ws):
    """Green -> yellow -> red scale on Risk / Severity columns."""
    for col_idx in range(1, ws.max_column + 1):
        header = ws.cell(row=1, column=col_idx).value or ""
        if "Risk" in str(header) or "Severity" in str(header):
            letter = get_column_letter(col_idx)
            ws.conditional_formatting.add(
                f"{letter}2:{letter}{ws.max_row}",
                ColorScaleRule(
                    start_type="min", start_color="63BE7B",
                    mid_type="percentile", mid_value=50,
                    mid_color="FFEB84",
                    end_type="max", end_color="F8696B",
                ),
            )
