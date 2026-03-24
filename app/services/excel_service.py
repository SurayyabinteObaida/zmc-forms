"""
excel_service.py
Generates Excel exports for each form category.
"""
import io
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
ALT_ROW_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
BORDER = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin")
)


def _apply_header(ws, headers):
    ws.append(headers)
    for col_idx, _ in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[1].height = 30


def _apply_row_style(ws, row_num, num_cols, is_alt):
    for col_idx in range(1, num_cols + 1):
        cell = ws.cell(row=row_num, column=col_idx)
        cell.border = BORDER
        cell.alignment = Alignment(vertical="center")
        if is_alt:
            cell.fill = ALT_ROW_FILL


def _auto_column_width(ws):
    for col in ws.columns:
        max_len = max((len(str(c.value or "")) for c in col), default=10)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 4, 40)


def generate_excel(form_type, records: list) -> bytes:
    """
    Generate Excel for a given form_type.
    records: list of ExtractedRecord objects with status='saved'
    Returns bytes of the xlsx file.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = form_type.name[:31]  # Excel sheet name limit

    enabled_fields = form_type.enabled_fields()
    headers = ["#", "File", "Saved At"] + [f.label for f in enabled_fields]

    _apply_header(ws, headers)

    for row_idx, record in enumerate(records, 1):
        data = json.loads(record.verified_data or "{}")
        row_data = [
            row_idx,
            record.filename or "",
            record.saved_at.strftime("%Y-%m-%d %H:%M") if record.saved_at else "",
        ]
        for f in enabled_fields:
            row_data.append(data.get(f.key, ""))

        ws.append(row_data)
        _apply_row_style(ws, row_idx + 1, len(headers), row_idx % 2 == 0)

    _auto_column_width(ws)
    ws.freeze_panes = "A2"

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()