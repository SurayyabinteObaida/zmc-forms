"""
extraction_service.py
Handles image-to-structured-data extraction via OpenAI Vision API (GPT-4o).
Two-layer validation: fuzzy matching + lookup validation.
Enhanced bottom-section field detection for waste fields.
"""
import os
import json
import base64
from datetime import datetime
from openai import OpenAI
from rapidfuzz import process, fuzz
from app.models import FormType


# ── Lookup Tables Import ───────────────────────────────────────────────────
try:
    from app.services.lookup_tables import LOOKUP_TABLES
    # Expected structure: {"job_name": [...], "printed_film": [...], "supplier": [...]}
    LOOKUP = LOOKUP_TABLES
except ImportError:
    # Fallback to hardcoded lookups if lookup_tables.py not available
    LOOKUP = {
        "job_name": [
            "147 STREET PIZZA", "14TH STREET PIZZA", "500 DIRHAM", "500 DIRHAM/AREENA",
            "ACCOUTR", "AESTHETIC GEN", "AJWA", "AL HABIB", "ANEELA'S", "ARAMEX",
            "ASIM JOFA", "BACHAA PATY", "BAGALLERY", "BEGALLERY", "BEJAAN HYGIEN",
            "BODY & BLAST", "BOURAQ EXPRESS", "BUZZAZI", "CHASE VALUE", "CHECKMATE",
            "COSMETICS CITY", "DADI JAN", "DARVAZA.PK", "DORUK", "DUNKIN", "DYNASTY",
            "ELEGANCIA", "EVOLUTION", "FASHION WEEK", "FINE FASHION", "FOCALLURE",
            "GRANNYS ORGANIC", "GRG", "HEMANI", "HIGH CLASS FABRICS", "HIGHFY",
            "INSTA MALL", "J. FABRICS BLACK", "J. FABRICS GREEN", "J.FABRIC GREEN",
            "J.FABRICS BLACK", "JAZMIN", "K-JUNCTION", "KHYBER MEDICAL", "LEZAAR VELOOR",
            "LITTLE PEOPLE", "LUXEURS", "LUXURU SOFT PACK", "LUXURY SOFT", "MAKEUP CITY",
            "MASTER", "MEJI BURGE BUN", "MEJI BURGER BUN", "MEJI RUSK", "MEJI RUSH",
            "MONAL FABRICS", "MOHSIN RASHID", "MT RUSK", "MT SPECIAL GOL RUSK", "MTJ",
            "O-TWO-O", "POLKA DOT", "POLKA DOT SALE", "POLKA DOT SOLVE TO GET 5% DISCOUNT",
            "RAJA FABIRCS", "RAJA FASHION", "RALVIL TEN", "RIDER", "RONIN",
            "SADAR APP", "SHOP REX", "SKY NET", "SMILE FINE TISSUE", "STITCHER",
            "TELEBRAND EXPRESS", "TOUHEED/HAQ HALAL", "TRIMCO", "TULIP", "UNIVERSAL",
            "UPS", "YAQOOB TEX", "ZAIB BY NIMSAY", "ZARPOSH", "ZED COURIER",
            "ZELLBURY", "ZURAJ",
        ],
        "printed_film": [
            "BOPP", "BOPP HOLO", "BOPP RAINBOW", "CPP", "EVA", "EVA MATT",
            "HD", "HD MILKY", "HD PURE", "M-PET", "MATT BOPP", "NON WOVEN",
            "PAPER", "PE", "PE 2 LAYER NATURAL/BLACK", "PE 2 LAYER NATURAL/MILKY",
            "PE 2 LAYER WHITE/BLACK", "PE 2 LAYER WHITE/GREY", "PE BLACK", "PE MILKY",
            "PE NATURAL", "PE PINK", "PET", "PIVA", "PP",
        ],
        "supplier": [
            "AFIL FODS", "AHMED HD", "BOPP", "CHWALA CORP", "G-PAK", "MACPAC",
            "MUNDIA EXPORT", "NOVATEX", "OLEFINS", "SALMAN BWANI", "SHABBIR PP",
            "SUBHAN", "U-FILER", "ZOHAIB", "ZMC",
        ],
    }


# ── Field Mapping & Thresholds ─────────────────────────────────────────────
# Maps extraction field keys to lookup categories
FIELD_LOOKUP_MAP = {
    "job_name": "job_name",
    "material": "printed_film",   # material field uses printed_film lookup
    "supplier": "supplier",
}

AUTO_CORRECT_THRESHOLD = 85   # ≥ this → silently auto-correct
SUGGEST_THRESHOLD = 60        # ≥ this → flag but still correct


def _get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ── Form Identification ────────────────────────────────────────────────────
FORM_IDENTIFICATION_PROMPT = """You are an expert at reading manufacturing production forms.
Look at this image carefully. Identify which type of form it is.

Known form types:
1. Flexo Printing Production Report (form code: F-PRD/01.2) - has fields like Cylinder Size, No. of Colors, Block #, Tube/Sheet, Bag Size
2. Gravure Printing Production Report (form code: F-PRD/01.1) - has fields like Cylinder Length x Cir, Color Man Ink GSM, Cylinder Qty

Respond with ONLY a JSON object:
{
  "form_code": "F-PRD/01.2" or "F-PRD/01.1" or "UNKNOWN",
  "confidence": 0.0 to 1.0,
  "reasoning": "brief reason"
}"""


def _build_extraction_prompt(form_type: FormType) -> str:
    """Build extraction prompt with enhanced field location instructions."""
    current_year = datetime.now().year
    enabled_fields = form_type.enabled_fields()
    field_list = "\n".join(
        f'  "{f.key}": <{f.field_type} or null if not visible>  # {f.label}'
        for f in enabled_fields
    )
    return f"""You are an expert at reading hand-filled manufacturing production forms.
Extract all visible field values from this {form_type.name}.

Return ONLY a valid JSON object with these exact keys (use null for any field not visible or illegible):
{{
{field_list}
}}

CRITICAL FIELD LOCATION INSTRUCTIONS:

1. DATE FIELD:
   - Look for a field labeled 'Date' or 'Print Date' near the top of the form
   - Date is typically handwritten in DD/MM/YYYY or DD-MM-YYYY format
   - Return exactly as written (e.g. "18/02/{current_year}")
   - If the year part looks wrong or unreadable, replace it with {current_year}

2. MATERIAL (Printed Film):
   - Find the cell labeled "Printed Film" in the mid-form section (alongside Web Size/Web Mic)
   - It contains a film type such as "PE 2 layer white/grey", "PE Milky", "BOPP", "PP", etc.
   - This is in the MIDDLE section of the form, NOT at the bottom

3. OPERATOR:
   - The form has an "Operator" column in the middle table where names repeat across rows
   - Also has an "Operator" signature line at the bottom of the form
   - Extract the unique operator name only ONCE — do NOT repeat or concatenate duplicate names
   - If two different operators appear (e.g. "Rizwan" and "Junaid"), return them as "Rizwan/Junaid"
   - If the same name appears multiple times, return it only once

4. BOTTOM SECTION WEIGHT FIELDS (VERY IMPORTANT):
   The bottom summary section has a 3-column layout. Read labels carefully:

   LEFT COLUMN (Plain side):
   - "plain_roll_wt": labeled "Plain G.wt" — the gross weight of plain rolls
     * Return as NUMBER
   - "plain_bal": labeled "Plain Bal" — plain balance weight
     * Return as NUMBER
   - "net_wt": labeled "Plain Net Wt." — this is in the BOTTOM-LEFT, last row before Remarks
     * This is DISTINCT from Printed Net Wt.
     * Typical value is smaller than Plain G.wt (e.g. if Plain G.wt=175.80, Plain Net Wt=77.80)
     * Return as NUMBER

   MIDDLE COLUMN (Printed side):
   - "printed_reel_wt": labeled "Printed Net Wt." — in the BOTTOM-MIDDLE section
     * This is DISTINCT from Plain Net Wt.
     * Typical value is close to but less than Printed G.wt
     * Return as NUMBER
   - "gross_wt": labeled "Printed G.wt" — gross weight of printed rolls
     * Return as NUMBER
   - "core_wt": labeled "Core Wt. B" in the bottom section
     * Return as NUMBER

5. BOTTOM SECTION WASTE FIELDS:
   RIGHT COLUMN of the bottom summary section:

   - "plain_waste": labeled "Plain Waste" — top of the right column
     * A dash (-) or blank means null, NOT zero
     * Return as NUMBER or null
   
   - "roll_waste": labeled "Roll Waste"
     * A dash (-) or blank means null
     * Return as NUMBER or null
   
   - "printed_waste": labeled "Printed Waste"
     * A dash (-) or blank means null
     * Return as NUMBER or null

   - "total_waste": labeled "Total Waste" — last row of the right column
     * This should equal the sum of all individual waste values
     * A dash (-) or blank means null
     * Return as NUMBER or null

6. OTHER NUMERIC FIELDS:
   For all other numeric fields (order_qty, speed, ink_gsm, etc.):
   - Return as NUMBER without units
   - If illegible or blank, use null

7. TEXT FIELDS:
   For text fields (job_name, job_code, etc.):
   - Extract exactly what is written
   - If illegible, use null
   - Do not calculate or infer values

REMEMBER:
- "Plain Net Wt." (net_wt) and "Printed Net Wt." (printed_reel_wt) are TWO DIFFERENT fields
- Plain Net Wt. is in the BOTTOM-LEFT. Printed Net Wt. is in the BOTTOM-MIDDLE.
- A dash (-) in any field means null, not zero."""


def _encode_image(image_path: str):
    """Encode image to base64 with proper media type detection."""
    ext = image_path.rsplit(".", 1)[-1].lower()
    media_type_map = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "webp": "image/webp", "gif": "image/gif"
    }
    media_type = media_type_map.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def _parse_json_response(text: str) -> dict:
    """Parse JSON response, handling markdown code blocks."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def _fix_date_year(value: str) -> str:
    """Replace suspicious years (not current year ±1) with current year."""
    if not value:
        return value
    current_year = datetime.now().year
    for sep in ("/", "-"):
        parts = value.split(sep)
        if len(parts) == 3:
            year_part = parts[2].strip()
            # Handle 2-digit year
            if len(year_part) == 2:
                full_year = int("20" + year_part) if int(year_part) < 50 else int("19" + year_part)
            elif len(year_part) == 4:
                full_year = int(year_part)
            else:
                full_year = current_year
            if abs(full_year - current_year) > 1:
                parts[2] = str(current_year)
            return sep.join(parts)
    return value


def _fuzzy_correct(extracted: dict) -> tuple[dict, dict]:
    """
    Layer 1: Apply fuzzy matching to lookup fields.
    Returns (corrected_data, corrections_log).
    corrections_log: {field: {original, corrected, score, auto}}
    """
    corrected = dict(extracted)
    log = {}

    for field_key, lookup_key in FIELD_LOOKUP_MAP.items():
        raw = corrected.get(field_key)
        if not raw or not isinstance(raw, str):
            continue

        candidates = LOOKUP.get(lookup_key, [])
        if not candidates:
            continue

        match, score, _ = process.extractOne(
            raw.upper(), [c.upper() for c in candidates],
            scorer=fuzz.token_sort_ratio
        )
        # Map back to original-cased candidate
        best = candidates[[c.upper() for c in candidates].index(match)]

        if score >= AUTO_CORRECT_THRESHOLD and best.upper() != raw.upper():
            log[field_key] = {"original": raw, "corrected": best, "score": score, "auto": True}
            corrected[field_key] = best
        elif score >= SUGGEST_THRESHOLD and best.upper() != raw.upper():
            log[field_key] = {"original": raw, "corrected": best, "score": score, "auto": True}
            corrected[field_key] = best  # still apply; UI can show it was auto-corrected

    return corrected, log


def _validate_against_lookup(data: dict) -> dict:
    """
    Layer 2: Check if values exist in master lookup tables.
    Returns validation_flags: {field: bool} where True = valid, False = not in lookup.
    """
    flags = {}
    
    for field_key, lookup_key in FIELD_LOOKUP_MAP.items():
        value = data.get(field_key)
        if not value or not isinstance(value, str):
            flags[field_key] = True  # null/empty values don't need validation
            continue
        
        candidates = LOOKUP.get(lookup_key, [])
        if not candidates:
            flags[field_key] = True  # no lookup available, skip validation
            continue
        
        # Check if value exists in lookup (case-insensitive)
        flags[field_key] = any(value.upper() == c.upper() for c in candidates)
    
    return flags


def _validate_waste_totals(data: dict) -> dict:
    """
    Post-processing: cross-check total_waste against sum of individual wastes.
    If total_waste is present but doesn't match the sum, recompute from parts.
    Handles common handwriting misread (e.g. 0.60 read as 6.6).
    """
    waste_fields = ["plain_waste", "roll_waste", "printed_waste", "setting_waste"]
    parts = [data.get(f) for f in waste_fields]
    numeric_parts = [float(v) for v in parts if v is not None]

    if not numeric_parts:
        return data

    computed_total = round(sum(numeric_parts), 3)
    extracted_total = data.get("total_waste")

    if extracted_total is None:
        data["total_waste"] = computed_total
        return data

    try:
        extracted_total = float(extracted_total)
    except (TypeError, ValueError):
        data["total_waste"] = computed_total
        return data

    # Allow 5% tolerance for rounding
    tolerance = max(0.05, computed_total * 0.05)
    if abs(extracted_total - computed_total) > tolerance:
        # Misread detected — replace with computed value
        data["total_waste"] = computed_total

    return data


def identify_form(image_path: str) -> dict:
    """Identify form type from image."""
    data, media_type = _encode_image(image_path)
    response = _get_client().chat.completions.create(
        model="gpt-4o",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}", "detail": "low"}},
                {"type": "text", "text": FORM_IDENTIFICATION_PROMPT},
            ],
        }],
    )
    return _parse_json_response(response.choices[0].message.content)


def extract_fields(image_path: str, form_type: FormType) -> dict:
    """Extract field values from image using GPT-4o Vision."""
    data, media_type = _encode_image(image_path)
    prompt = _build_extraction_prompt(form_type)
    response = _get_client().chat.completions.create(
        model="gpt-4o",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}", "detail": "high"}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return _parse_json_response(response.choices[0].message.content)


def process_image(image_path: str, form_types: list) -> dict:
    """
    Main entry point: Process image with two-layer validation.
    
    Returns:
        {
            "form_code": str,
            "form_type_id": int,
            "data": dict,              # corrected values
            "raw_data": dict,          # original OCR output
            "corrections": dict,       # fuzzy matching corrections
            "validation_flags": dict,  # lookup validation results
            "confidence": float,
            "error": str or None
        }
    """
    try:
        # Step 1: Identify form type
        id_result = identify_form(image_path)
        form_code = id_result.get("form_code", "UNKNOWN")
        confidence = id_result.get("confidence", 0.0)

        matched_form = next((ft for ft in form_types if ft.code == form_code), None)
        if not matched_form:
            return {
                "form_code": form_code,
                "form_type_id": None,
                "data": {},
                "confidence": confidence,
                "error": f"Could not match form code '{form_code}'."
            }

        # Step 2: Extract fields
        extracted = extract_fields(image_path, matched_form)

        # Step 3: Fix date year
        for date_key in ("date", "print_date"):
            if extracted.get(date_key):
                extracted[date_key] = _fix_date_year(str(extracted[date_key]))

        # Step 4: Layer 1 - Fuzzy-correct lookup fields
        corrected, corrections = _fuzzy_correct(extracted)

        # Step 5: Layer 2 - Validate against lookup tables
        validation_flags = _validate_against_lookup(corrected)

        # Step 6: Cross-check waste totals
        corrected = _validate_waste_totals(corrected)

        return {
            "form_code": form_code,
            "form_type_id": matched_form.id,
            "data": corrected,              # corrected values
            "raw_data": extracted,          # original before correction
            "corrections": corrections,     # audit log for UI display
            "validation_flags": validation_flags,  # NEW: lookup validation flags
            "confidence": confidence,
            "error": None,
        }

    except json.JSONDecodeError as e:
        return {
            "form_code": None,
            "form_type_id": None,
            "data": {},
            "confidence": 0.0,
            "error": f"JSON parse error: {str(e)}"
        }
    except Exception as e:
        return {
            "form_code": None,
            "form_type_id": None,
            "data": {},
            "confidence": 0.0,
            "error": str(e)
        }