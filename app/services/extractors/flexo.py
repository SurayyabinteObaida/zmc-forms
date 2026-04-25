"""
extractors/flexo.py
Extraction logic for Flexo Printing Production Report (F-PRD/01.2).
"""
from datetime import datetime
from app.models import FormType
from app.services.extractors.base import (
    vision_call, parse_json, fix_date_year,
    fuzzy_correct, validate_against_lookup, validate_waste_totals,
)

FIELD_LOOKUP_MAP = {
    "job_name": "job_name",
    "material":  "printed_film",
    "supplier":  "supplier",
}


def _build_prompt(form_type: FormType) -> str:
    current_year = datetime.now().year
    field_list = "\n".join(
        f'  "{f.key}": <{f.field_type} or null>  # {f.label}'
        for f in form_type.enabled_fields()
    )
    return f"""You are an expert at reading hand-filled Flexo Printing Production forms (F-PRD/01.2).
Extract all visible field values.

Return ONLY a valid JSON object with these exact keys (null for any field not visible or illegible):
{{
{field_list}
}}

FIELD LOCATION INSTRUCTIONS:

DATE:
- Look for field labeled 'Date' near the top. Format: DD/MM/YYYY or DD-MM-YYYY.
- Return exactly as written. If year looks wrong, replace with {current_year}.

MATERIAL (Printed Film):
- Find "Printed Film" in the mid-form section. Contains film types like "PE 2 layer white/grey", "BOPP", "PP".

OPERATOR:
- Extract unique operator name once. If two different operators appear, return "Name1/Name2".

BOTTOM SECTION — WEIGHT FIELDS:
LEFT COLUMN (Plain side):
  "plain_roll_wt"   → labeled "Plain G.wt" (NUMBER)
  "plain_bal"       → labeled "Plain Bal" (NUMBER)
  "net_wt"          → labeled "Plain Net Wt." — LAST row of left column (NUMBER)
    Verify: Plain Net Wt = Plain G.wt − Plain Bal − Core Wt. A

MIDDLE COLUMN (Printed side):
  "gross_wt"        → labeled "Printed G.wt" — FIRST row (NUMBER)
  "core_wt"         → labeled "Core Wt. B" — SECOND row (NUMBER)
  "printed_reel_wt" → labeled "Printed Net Wt." — THIRD row (NUMBER)
    Verify: Printed Net Wt = Printed G.wt − Core Wt. B

BOTTOM SECTION — WASTE FIELDS (RIGHT COLUMN):
  "plain_waste"    → "Plain Waste"   (NUMBER or null — dash/blank = null)
  "roll_waste"     → "Roll Waste"    (NUMBER or null)
  "printed_waste"  → "Printed Waste" (NUMBER or null)
  "total_waste"    → "Total Waste"   (NUMBER or null — should equal sum of all wastes)

RULES:
- Return numbers without units.
- A dash (-) or blank always means null, never zero.
- "Plain Net Wt." and "Printed Net Wt." are TWO DIFFERENT fields."""


def extract(image_path: str, form_type: FormType) -> dict:
    """
    Extract fields from a Flexo Printing form image.
    Returns: {data, corrections, validation_flags}
    """
    raw = vision_call(image_path, _build_prompt(form_type), max_tokens=2048, detail="high")
    data = parse_json(raw)

    if data.get("date"):
        data["date"] = fix_date_year(str(data["date"]))

    data, corrections = fuzzy_correct(data, FIELD_LOOKUP_MAP)
    validation_flags = validate_against_lookup(data, FIELD_LOOKUP_MAP)
    data = validate_waste_totals(data)

    return {
        "data": data,
        "corrections": corrections,
        "validation_flags": validation_flags,
    }
