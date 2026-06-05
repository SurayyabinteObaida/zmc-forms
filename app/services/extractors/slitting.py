"""
extractors/slitting.py
Extraction logic for Slitting Production Report (F-PRD/03.1).
"""
from app.services.extractors.base import (
    vision_call, parse_json, fix_date_year,
    fuzzy_correct, validate_against_lookup,
)

FIELD_LOOKUP_MAP = {
    "job_name": "job_name",
}

_PROMPT = """You are an expert at reading hand-filled Slitting Production forms (F-PRD/03.1).
Extract the header fields and summary totals. Do NOT extract individual roll table rows.

Return ONLY a valid JSON object with this exact structure (null for any field not visible or illegible):

{
  "job_code": "<string>",
  "date": "<string — date as written>",
  "job_name": "<string>",
  "structure": "<string — e.g. 'PET/PE' or material description>",
  "overall_mic": "<string — micron value>",
  "slitting_size": "<string>",
  "outter_dia": "<string>",
  "inner_dia": "<string>",
  "start_time": "<string>",
  "end_time": "<string>",
  "operator": "<string>",
  "shift": "<string>",
  "total_mother_reels": <number or null>,
  "total_slitted_reels": <number or null>,
  "single_slitted_reel_wt": <number or null>,
  "slitted_reel_wt": <number or null>,
  "mother_reel_wt": <number or null>,
  "setting_wastage": <number or null>,
  "trim_waste": <number or null>,
  "trim_size": "<string or null>",
  "remarks": "<string or null>"
}

FIELD LOCATION INSTRUCTIONS:

HEADER (top section):
- DATE: top area, labeled "Date"
- JOB NAME: top area, labeled "Job Name"
- JOB CODE: top area, labeled "Job Code"
- WEB SIZE: labeled "Web Size" — the original reel width
- SLITTING SIZE: labeled "Slitting Size" — the cut width(s)
- MATERIAL / STRUCTURE: labeled "Material" — e.g. "Plain", "Laminated", "Printed"
- OUTTER DIA: labeled "Outer Dia"
- INNER DIA: labeled "Inner Dia"
- DIRECTION: if present
- START TIME, END TIME: time fields
- OPERATOR: labeled "Operator"
- SPEED: if present

SUMMARY (bottom section):
- SLITTED WEIGHT / SLITTED REEL WT.: total weight of slitted reels
- MOTHER REEL WT: weight of the mother reel(s) before slitting
- NET WT.: net weight
- SETTING WASTE: labeled "Setting Waste"
- TRIM WASTE: labeled "Trim Waste"
- TOTAL WASTE: labeled "Total Waste" (skip — formula column)
- CORE WT.: various core weights (may appear multiple times)

RULES:
- Numbers must be returned as numbers, not strings.
- A dash (-) or blank always means null, never zero.
- Ignore individual roll rows in the middle table.
- STRUCTURE comes from the "Material" field — could be "Plain", "Laminated", "Printed", or a material code."""


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
