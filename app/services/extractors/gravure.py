"""
extractors/gravure.py
Extraction logic for Gravure Printing Production Report (F-PRD/01.1).
"""
from datetime import datetime
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
Extract ALL visible field values from this form.

Return ONLY a valid JSON object with this exact structure (null for any field not visible or illegible):

{
  "print_date": "<string — date as written>",
  "job_name": "<string>",
  "job_code": "<string>",
  "plain_order_qty": <number or null>,
  "material": "<string — film/material type>",
  "material_supplier": "<string>",
  "web_size_mic": "<string — e.g. '28 / 60'>",
  "cylinder_qty_number": "<string>",
  "cylinder_length_cir": "<string>",
  "speed": <number or null>,
  "operator": "<string>",
  "color_man": "<string>",
  "ink_gsm": <number or null>,
  "setting_time": "<string>",
  "start_time": "<string>",
  "end_time": "<string>",

  "roll_rows": [
    {
      "rm_number": "<string>",
      "plain_roll_wt": <number or null>,
      "plain_balance_rejected": <number or null>,
      "plain_core_wt": <number or null>,
      "printed_roll_number": "<string>",
      "printed_roll_wt": <number or null>,
      "printed_core_wt": <number or null>,
      "meter": <number or null>,
      "remarks": "<string or null>"
    }
  ],

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
  "total_waste": <number or null>,

  "prepared_by": "<string>",
  "supervisor": "<string>",
  "remarks": "<string or null>"
}

FIELD LOCATION INSTRUCTIONS:

HEADER (top section):
- PRINT DATE: top-left, labeled "Print Date"
- JOB NAME: top center
- JOB CODE: top right
- PLAIN ORDER QTY, MATERIAL, WEB SIZE & MIC: second row
- CYLINDER QTY & #, MATERIAL SUPPLIER: third row
- CYLINDER LENGTH X CIR: fourth row
- SPEED: single value field
- OPERATOR, COLOR MAN, INK GSM: operator section row

ROLL TABLE (repeating rows, middle section):
- Each row is one RM roll. Extract EVERY non-empty row.
- Columns left to right: RM #, PLAIN ROLL WT., PLAIN BALANCE REJECTED,
  PLAIN CORE WT., PRINTED ROLL #, PRINTED ROLL WT., PRINTED CORE WT., METER, REMARKS
- Only include rows where at least one field has a value. Skip fully blank rows.
- If no rows are filled, return roll_rows as [].

FOOTER (bottom summary section):
LEFT side:
  "plain_gross_wt"   → "Plain Gross Wt."
  "plain_core_wt"    → "Plain Core Wt."
  "plain_balance"    → "Plain Balance"
  "plain_net_wt"     → "Plain Net Wt."

RIGHT side:
  "printed_gross_wt" → "Printed Gross Wt."
  "printed_core_wt"  → "Printed Core Wt."
  "printed_net_wt"   → "Printed Net Wt."
  "total_mtr"        → "Total Mtr."

WASTE (far right column):
  "plain_waste"    → "Plain Waste"
  "roll_waste"     → "Roll Waste"
  "printed_waste"  → "Printed Waste"
  "setting_waste"  → "Setting Waste"
  "total_waste"    → "Total Waste" (should equal sum of all individual wastes)

SIGNATURES (bottom lines):
  "prepared_by", "supervisor"

RULES:
- Numbers must be returned as numbers, not strings.
- A dash (-) or blank always means null, never zero.
- Do NOT include roll_rows entries that are entirely blank."""


def extract(image_path: str) -> dict:
    """
    Extract fields from a Gravure Printing form image.
    Returns: {data, corrections, validation_flags}
    """
    raw = vision_call(image_path, _PROMPT, max_tokens=4096, detail="high")
    data = parse_json(raw)

    if data.get("print_date"):
        data["print_date"] = fix_date_year(str(data["print_date"]))

    # Separate roll_rows before fuzzy correction (only correct header-level fields)
    roll_rows = data.pop("roll_rows", []) or []

    data, corrections = fuzzy_correct(data, FIELD_LOOKUP_MAP)
    validation_flags = validate_against_lookup(data, FIELD_LOOKUP_MAP)
    data = validate_waste_totals(data)

    # Put roll_rows back
    data["roll_rows"] = roll_rows

    return {
        "data": data,
        "corrections": corrections,
        "validation_flags": validation_flags,
    }
