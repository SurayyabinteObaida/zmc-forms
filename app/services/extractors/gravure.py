"""
extractors/gravure.py
Extraction logic for Gravure Printing Production Report (F-PRD/01.1).
Extracts header fields and footer summary fields only.
"""
from app.services.extractors.base import (
    vision_call, parse_json, fix_date_year,
    fuzzy_correct, validate_against_lookup, validate_waste_totals,
)

FIELD_LOOKUP_MAP = {
    "job_name":          "job_name",
    "material":          "printed_film",
    "material_supplier": "supplier",
}

_PROMPT = """You are an expert at reading hand-filled Gravure Printing Production forms (F-PRD/01.1).
Extract ONLY the header fields and footer summary fields. Do NOT extract the roll table rows.

Return ONLY a valid JSON object with this exact structure (null for any field not visible or illegible):

{
  "print_date": "<string — date as written>",
  "job_name": "<string>",
  "job_code": "<string>",
  "plain_order_qty": <number or null>,
  "material": "<string — film/material type>",
  "material_supplier": "<string>",
  "web_size_mic": "<string — e.g. '1150 / 65'>",
  "cylinder_qty_number": "<string — e.g. '06 2505243'>",
  "cylinder_length_cir": "<string — e.g. '1300x560'>",
  "speed": <number or null>,
  "operator": "<string>",
  "color_man": "<string>",
  "ink_gsm": <number or null>,
  "setting_time": "<string>",
  "start_time": "<string>",
  "end_time": "<string>",

  "plain_gross_wt": <number or null>,
  "printed_gross_wt": <number or null>,
  "plain_core_wt": <number or null>,
  "printed_core_wt": <number or null>,
  "plain_balance": <number or null>,
  "plain_net_wt": <number or null>,
  "printed_net_wt": <number or null>,
  "total_mtr": <number or null>,
  "plain_waste": <number or null>,
  "roll_waste": <number or null>,
  "printed_waste": <number or null>,
  "setting_waste": <number or null>,
  "total_waste": <number or null>
}

FIELD LOCATION INSTRUCTIONS:

HEADER (top section of form):
- PRINT DATE: top-left, labeled "Print Date"
- JOB NAME: top center
- JOB CODE: top right
- PLAIN ORDER QTY: left side, second row
- MATERIAL: center, second row
- WEB SIZE & MIC: right side, second row — two values separated by a space or slash
- CYLINDER QTY & #: left side, third row — quantity + cylinder number(s)
- MATERIAL SUPPLIER: center, third row
- SETTING TIME, START TIME, END TIME: right side, third row
- CYLINDER LENGTH X CIR: left side, fourth row
- SPEED: center, fourth row
- OPERATOR: left side, fifth row
- COLOR MAN: center, fifth row
- INK GSM: right side, fifth row

FOOTER (bottom summary section — below the roll table):
LEFT column:
  "plain_gross_wt"  → labeled "Plain Gross Wt."
  "plain_core_wt"   → labeled "Plain Core Wt."
  "plain_balance"   → labeled "Plain Balance"
  "plain_net_wt"    → labeled "Plain Net Wt."

RIGHT column:
  "printed_gross_wt" → labeled "Printed Gross Wt."
  "printed_core_wt"  → labeled "Printed Core Wt."
  "printed_net_wt"   → labeled "Printed Net Wt."
  "total_mtr"        → labeled "Total Mtr."

WASTE (far right):
  "plain_waste"    → "Plain Waste"
  "roll_waste"     → "Roll Waste"
  "printed_waste"  → "Printed Waste" (a dash means null)
  "setting_waste"  → "Setting Waste"
  "total_waste"    → "Total Waste"

RULES:
- Numbers must be returned as numbers, not strings.
- A dash (-) or blank always means null, never zero.
- Ignore the roll table in the middle of the form entirely."""


def extract(image_path: str) -> dict:
    raw = vision_call(image_path, _PROMPT, max_tokens=2048, detail="high")
    data = parse_json(raw)

    if data.get("print_date"):
        data["print_date"] = fix_date_year(str(data["print_date"]))

    data, corrections = fuzzy_correct(data, FIELD_LOOKUP_MAP)
    validation_flags = validate_against_lookup(data, FIELD_LOOKUP_MAP)
    data = validate_waste_totals(data)

    return {
        "data": data,
        "corrections": corrections,
        "validation_flags": validation_flags,
    }