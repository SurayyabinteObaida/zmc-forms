"""
excel_service.py
Generates Excel exports — full batch and per-batch — in Serial Wise Data format.
Export columns are user-configurable and persisted in export_config.json.
"""
import io
import json
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── Config persistence ────────────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "export_config.json")

# Master column definition: (display_label, data_key, width, is_formula)
# data_key matches EXACTLY the field keys in FlexoPrintingRecord / FieldConfig
ALL_COLUMNS = [
    ("S. NO",             "serial",        6,  False),
    ("Job Code",          "job_code",      14, False),
    ("PRINT DATE",        "date",          12, False),
    ("Job Name",          "job_name",      22, False),
    ("BAG SIZE",          "bag_size",      14, False),
    ("PRINTED FILM",      "material",      18, False),   # field key = material
    ("TUBE / SHEET",      "tube_sheet",    12, False),
    ("SIZE (INCHES)",     "web_size",      12, False),
    ("FILM SUPPLIER",     "supplier",      15, False),   # field key = supplier
    ("ORDER QTY",         "order_qty",     10, False),
    ("PLAIN WT",          "core_wt",       10, False),   # field key = core_wt
    ("PRINTED WT",        "net_wt",        10, False),   # field key = net_wt
    ("Printed Wastage",   "printed_waste", 12, False),
    ("PLAIN WASTAGE",     "plain_waste",   12, False),
    ("OPERATOR",          "operator",      12, False),
    ("SETTING TIME",      "setting_time",  12, False),
    ("START TIME",        "start_time",    10, False),
    ("END TIME",          "end_time",      10, False),
    ("Wt. Gain",          "_wt_gain",      10, True),
    ("Wt. Gain %",        "_wt_gain_pct",  10, True),
    ("Wastage IN %",      "_wastage_pct",  10, True),
    ("SIZE IN MM",        "_size_mm",      12, True),
    ("DENSITY",           "mic",           10, False),   # field key = mic
    ("CALCULATED METERS", "_calc_meters",  16, True),
    ("MACHINE RUN TIME",  "_run_time",     14, True),
    ("AVG ACTUAL SPEED",  "_avg_speed",    14, True),
    ("SHIFT",             "shift",          8, False),
    ("Run Hrs (24H)",     "_run_hrs",      10, True),
    ("NO. OF STOPS",      "machine_stops", 10, False),
    ("JOB STATUS",        "job_status",    12, False),
]

MANDATORY_KEYS = {"serial"}


def _default_config():
    return {col[1]: True for col in ALL_COLUMNS}


def load_export_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                saved = json.load(f)
            cfg = _default_config()
            cfg.update(saved)
            return cfg
        except Exception:
            pass
    return _default_config()


def save_export_config(config: dict):
    for k in MANDATORY_KEYS:
        config[k] = True
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def get_active_columns(config=None):
    if config is None:
        config = load_export_config()
    return [col for col in ALL_COLUMNS if config.get(col[1], True)]


# ── Styles ────────────────────────────────────────────────────────────────────
HEADER_FILL     = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT     = Font(color="FFFFFF", bold=True, size=10, name="Arial")
ALT_ROW_FILL    = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
CORRECTION_FILL = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
THIN   = Side(style="thin")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _col(idx):
    return get_column_letter(idx)


def _apply_header(ws, headers, row=1):
    for ci, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=ci)
        c.value = h
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[row].height = 32


def _style_data_row(ws, row, ncols, alt, corrected_cols=None):
    for ci in range(1, ncols + 1):
        c = ws.cell(row=row, column=ci)
        c.border = BORDER
        c.alignment = Alignment(vertical="center")
        if corrected_cols and ci in corrected_cols:
            c.fill = CORRECTION_FILL
        elif alt:
            c.fill = ALT_ROW_FILL


def _auto_col_width(ws):
    for col in ws.columns:
        w = max((len(str(c.value or "")) for c in col), default=10)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(w + 4, 40)


def _get_data(record):
    raw = getattr(record, "verified_data", None) \
       or getattr(record, "raw_extraction", None) \
       or "{}"
    return json.loads(raw)


def _write_serial_wise(ws, records, corrections_map=None, config=None):
    corrections_map = corrections_map or {}
    active_cols = get_active_columns(config)
    headers = [c[0] for c in active_cols]
    ncols = len(headers)
    _apply_header(ws, headers, row=1)

    col_of = {c[1]: i + 1 for i, c in enumerate(active_cols)}

    for row_idx, record in enumerate(records, 1):
        excel_row = row_idx + 1
        data = _get_data(record)
        corrections = corrections_map.get(record.id, {})

        corrected_ci = {col_of[fk] for fk in corrections if fk in col_of}

        if "serial" in col_of:
            ws.cell(excel_row, col_of["serial"]).value = row_idx

        for label, dk, width, is_formula in active_cols:
            if is_formula or dk == "serial":
                continue
            ws.cell(excel_row, col_of[dk]).value = data.get(dk) or ""

        r = excel_row

        def fc(key):
            return _col(col_of[key]) if key in col_of else None

        pw   = fc("core_wt")
        prw  = fc("net_wt")
        plw  = fc("plain_waste")
        st   = fc("start_time")
        et   = fc("end_time")
        dens = fc("mic")
        ws_c = fc("web_size")

        if "_wt_gain" in col_of and pw and prw:
            ws.cell(r, col_of["_wt_gain"]).value = \
                f"=IF(AND({prw}{r}<>\"\",{pw}{r}<>\"\"),{prw}{r}-{pw}{r},\"\")"

        if "_wt_gain_pct" in col_of and pw and prw:
            c = ws.cell(r, col_of["_wt_gain_pct"])
            c.value = f"=IF(AND({pw}{r}<>0,{pw}{r}<>\"\"),({prw}{r}-{pw}{r})/{pw}{r},\"\")"
            c.number_format = "0.0%"

        if "_wastage_pct" in col_of and pw and plw:
            c = ws.cell(r, col_of["_wastage_pct"])
            c.value = f"=IF(AND({pw}{r}<>0,{plw}{r}<>\"\"),{plw}{r}/{pw}{r},\"\")"
            c.number_format = "0.0%"

        if "_size_mm" in col_of and ws_c:
            ws.cell(r, col_of["_size_mm"]).value = \
                f"=IF({ws_c}{r}<>\"\",{ws_c}{r}*25.4,\"\")"

        if "_calc_meters" in col_of and pw and ws_c and dens:
            ws.cell(r, col_of["_calc_meters"]).value = \
                f"=IF(AND({pw}{r}<>\"\",{ws_c}{r}<>\"\",{dens}{r}<>\"\")," \
                f"({pw}{r}*1000000)/({ws_c}{r}*25.4/1000*{dens}{r}),\"\")"

        rt_col = fc("_run_time")
        if "_run_time" in col_of and st and et:
            ws.cell(r, col_of["_run_time"]).value = \
                f"=IF(AND({st}{r}<>\"\",{et}{r}<>\"\"),{et}{r}-{st}{r},\"\")"

        if "_run_hrs" in col_of and rt_col:
            ws.cell(r, col_of["_run_hrs"]).value = \
                f"=IF({rt_col}{r}<>\"\",{rt_col}{r}*24,\"\")"

        calc_c = fc("_calc_meters")
        rh_c   = fc("_run_hrs")
        if "_avg_speed" in col_of and calc_c and rh_c:
            ws.cell(r, col_of["_avg_speed"]).value = \
                f"=IF(AND({calc_c}{r}<>\"\",{rh_c}{r}<>0),{calc_c}{r}/{rh_c}{r},\"\")"

        _style_data_row(ws, excel_row, ncols, row_idx % 2 == 0, corrected_ci)

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{_col(ncols)}1"
    for i, (_, _, width, _) in enumerate(active_cols, 1):
        ws.column_dimensions[_col(i)].width = width


# ── Public API ────────────────────────────────────────────────────────────────

def generate_excel(form_type, records, corrections_map=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Serial Wise Data"
    _write_serial_wise(ws, records, corrections_map)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def generate_batch_excel(batch_id, records, corrections_map=None):
    config = load_export_config()
    wb = Workbook()

    ws_serial = wb.active
    ws_serial.title = "Serial Wise Data"
    _write_serial_wise(ws_serial, records, corrections_map, config)

    ws_raw = wb.create_sheet("Raw Data")
    raw_headers = ["#", "File", "Saved At", "Date", "Job Name", "Job Code", "Operator",
                   "Material", "Supplier", "Web Size", "Mic", "Ink GSM", "Tube/Sheet",
                   "Bag Size", "Setting Time", "Start Time", "End Time",
                   "Plain Net Wt.", "Plain Waste", "Printed Net Wt.", "Printed Waste"]
    _apply_header(ws_raw, raw_headers)
    for ri, record in enumerate(records, 1):
        data = _get_data(record)
        saved_at = record.saved_at.strftime("%Y-%m-%d %H:%M") if record.saved_at else ""
        row = [
            ri, record.filename or "", saved_at,
            data.get("date", ""), data.get("job_name", ""), data.get("job_code", ""),
            data.get("operator", ""), data.get("material", ""), data.get("supplier", ""),
            data.get("web_size", ""), data.get("mic", ""), data.get("ink_gsm", ""),
            data.get("tube_sheet", ""), data.get("bag_size", ""),
            data.get("setting_time", ""), data.get("start_time", ""), data.get("end_time", ""),
            data.get("core_wt", ""), data.get("plain_waste", ""),
            data.get("net_wt", ""), data.get("printed_waste", ""),
        ]
        ws_raw.append(row)
        _style_data_row(ws_raw, ri + 1, len(raw_headers), ri % 2 == 0)
    _auto_col_width(ws_raw)
    ws_raw.freeze_panes = "A2"

    wb.properties.title = f"Batch {batch_id} — {datetime.now().strftime('%Y-%m-%d')}"
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def get_column_config_for_ui():
    """Return all columns with current enabled state for the settings UI."""
    config = load_export_config()
    return [
        {
            "key": col[1],
            "label": col[0],
            "enabled": config.get(col[1], True),
            "mandatory": col[1] in MANDATORY_KEYS,
            "is_formula": col[3],
        }
        for col in ALL_COLUMNS
    ]