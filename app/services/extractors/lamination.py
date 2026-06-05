"""
extractors/lamination.py
Extraction logic for Lamination Production Report (F-PRD/02.1).
"""
from app.services.extractors.base import (
    vision_call, parse_json, fix_date_year,
    fuzzy_correct, validate_against_lookup,
)

FIELD_LOOKUP_MAP = {
    "job_name": "job_name",
}

_PROMPT = """You are an expert at reading hand-filled Lamination Production forms (F-PRD/02.1).
Extract the header fields and summary totals. Do NOT extract individual roll table rows.

Return ONLY a valid JSON object with this exact structure (null for any field not visible or illegible):

{
  "job_code": "<string>",
  "stage_code": "<string — 1, 2, or 3>",
  "month": "<string>",
  "date": "<string — date as written>",
  "job_name": "<string>",
  "machine": "<string>",
  "shift": "<string>",
  "speed": <number or null>,
  "start_time": "<string>",
  "end_time": "<string>",
  "structure": "<string — e.g. 'PET/PE'>",
  "film_a": "<string — printed material name>",
  "film_a_size_micron": "<string — e.g. '1050 / 12'>",
  "film_b": "<string — laminated material name>",
  "film_b_size_micron": "<string — e.g. '1050 / 50'>",
  "glue_coating_size": "<string>",
  "total_printed_film_qty": <number or null>,
  "printed_wastage": <number or null>,
  "total_film_b_qty": <number or null>,
  "film_b_wastage": <number or null>,
  "total_order_qty": <number or null>,
  "total_laminated_qty": <number or null>,
  "job_status": "<string>",
  "total_laminated_meters": <number or null>,
  "laminated_wastage": <number or null>,
  "glue_ratio": "<string — e.g. '100:5:50'>",
  "glue_type": "<string>",
  "hardner": <number or null>,
  "resin": <number or null>,
  "ethyl_acetate": <number or null>,
  "remarks": "<string or null>"
}

FIELD LOCATION INSTRUCTIONS:

HEADER (top section):
- JOB CODE: top-left
- DATE: top area
- JOB NAME: top center
- TARGET QTY: labeled "Target Qty"
- PRINTED MATERIAL / FILM A: labeled "Printed Material"
- FILM SUPPLIER: labeled "Film Supplier"
- LAMINATED MATERIAL / FILM B: labeled "Laminated Material"
- WEB SIZE / MIC: labeled "Web Size / Mic" — applies to both films
- SETTING TIME, START TIME, END TIME: time fields
- GLUE GSM / GLUE COATING SIZE: labeled area
- INK GSM: if present
- GLUE SUPPLIER: labeled "Glue Supplier"
- MACHINE SPEED / SPEED: labeled "Machine Speed"
- GLUE RATIO: labeled "Glue Ratio" — format like "100:5:50"
- OPERATOR: labeled "Operator"

LAYER SECTIONS (middle):
- 1ST LAYER (A LAYER): G.Wt., Core Wt., Balance/Rejected, Net Wt.
- 2ND LAYER (B LAYER): G.Wt., Core Wt., Balance/Rejected, Net Wt.
- LAMINATED WT: G.Wt., Core Wt., Net Wt., Meter

WASTAGE DETAILS:
- A FILM WASTE → printed_wastage
- B FILM WASTE → film_b_wastage
- LAM WASTE → laminated_wastage

CHEMICALS (bottom):
- HARDNER, RESIN, ETHYL ACETATE: numeric values

RULES:
- Numbers must be returned as numbers, not strings.
- A dash (-) or blank always means null, never zero.
- STAGE CODE: 1 = first lamination, 2 = second, 3 = third layer.
- Ignore individual roll rows in the middle table."""


def extract(image_path: str) -> dict:
    raw = vision_call(image_path, _PROMPT, max_tokens=2048, detail="high")
    data = parse_json(raw)

    if data.get("date"):
        data["date"] = fix_date_year(str(data["date"]))

    data, corrections = fuzzy_correct(data, FIELD_LOOKUP_MAP)
    validation_flags = validate_against_lookup(data, FIELD_LOOKUP_MAP)

    return {
        "data": data,
        "corrections": corrections,
        "validation_flags": validation_flags,
    }
