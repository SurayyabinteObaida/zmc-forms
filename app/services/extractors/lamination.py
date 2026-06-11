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
  "speed": <number or null — from the "Machine Speed" field ONLY, never from "Web Size / Mic">,
  "start_time": "<string>",
  "end_time": "<string>",
  "structure": "<string — e.g. 'PET/PE'>",
  "film_a": "<string — printed material name>",
  "film_a_size_micron": "<string — e.g. '1050 / 12'>",
  "film_b": "<string — laminated material name>",
  "film_b_size_micron": "<string — e.g. '1050 / 50'>",
  "glue_coating_size": "<string>",
  "total_printed_film_qty": <number or null — A Layer NET WT., not G.Wt.>,
  "printed_wastage": <number or null>,
  "total_film_b_qty": <number or null — B Layer NET WT., not G.Wt.>,
  "film_b_wastage": <number or null>,
  "total_order_qty": <number or null>,
  "total_laminated_qty": <number or null — Laminated NET WT., not G.Wt.>,
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
- WEB SIZE / MIC: labeled "Web Size / Mic" — applies to both films. NEVER use this value for "speed".
- SETTING TIME, START TIME, END TIME: time fields
- GLUE GSM / GLUE COATING SIZE: labeled area
- INK GSM: if present
- GLUE SUPPLIER: labeled "Glue Supplier"
- MACHINE SPEED / SPEED: take ONLY from the field explicitly labeled "Machine Speed". If no "Machine Speed" label is visible, return null for "speed" — do not substitute Web Size, Mic, or any other number.
- GLUE RATIO: labeled "Glue Ratio" — format like "100:5:50"
- OPERATOR: labeled "Operator"

LAYER SECTIONS (middle):
- 1ST LAYER (A LAYER): columns are G.Wt., Core Wt., Balance/Rejected, Net Wt. → return the NET WT. value as "total_printed_film_qty". Do NOT use G.Wt.
- 2ND LAYER (B LAYER): columns are G.Wt., Core Wt., Balance/Rejected, Net Wt. → return the NET WT. value as "total_film_b_qty". Do NOT use G.Wt.
- LAMINATED WT: columns are G.Wt., Core Wt., Net Wt., Meter → return the NET WT. value as "total_laminated_qty" and the Meter value as "total_laminated_meters". Do NOT use G.Wt.

WASTAGE DETAILS:
- A FILM WASTE → printed_wastage
- B FILM WASTE → film_b_wastage
- LAM WASTE → laminated_wastage

CHEMICALS (bottom):
- HARDNER, RESIN, ETHYL ACETATE: numeric values

RULES:
- All three weight fields ("total_printed_film_qty", "total_film_b_qty", "total_laminated_qty") must come from NET WT. values. If both G.Wt. and Net Wt. are visible for a layer, always use Net Wt. — never the gross value.
- "speed" must come only from the "Machine Speed" field. Web Size / Mic values are widths in mm/microns, not speeds — never place them in "speed".
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