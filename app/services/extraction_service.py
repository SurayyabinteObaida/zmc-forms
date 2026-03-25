"""
extraction_service.py
Handles image-to-structured-data extraction via OpenAI Vision API (GPT-4o).
Includes fuzzy matching for job_name, printed_film, supplier fields.
"""
import os
import json
import base64
from datetime import datetime
from openai import OpenAI
from rapidfuzz import process, fuzz
from app.models import FormType


# ── Lookup tables (generated from FLEXO_PRINTING_MASTER.xlsx) ──────────────
LOOKUP = {
    "job_name": [
        "FOCALLURE","TOUHEED/HAQ HALAL","SADAR APP","EVOLUTION","MTJ","DORUK","DUNKIN","RONIN",
        "LUXEURS","CHECKMATE","MEJI BURGE BUN","MEJI RUSK","POLKA DOT","SKY NET","SHOP REX",
        "DADI JAN","ZARPOSH","POLKA DOT SALE","MEJI BURGER BUN","MT SPECIAL GOL RUSK","BUZZAZI",
        "LITTLE PEOPLE","BEGALLERY","147 STREET PIZZA","HEMANI","MONAL FABRICS","J.FABRIC GREEN",
        "J.FABRICS BLACK","INSTA MALL","FINE FASHION","BACHAA PATY","BEJAAN HYGIEN",
        "BAR TOWELS 75 PACK","LUXURU SOFT PACK","BAR TOWELS 24 PACK","MAKEUP CITY","DARVAZA.PK",
        "STITCHER","GRANNYS ORGANIC","HIGHFY","ZELLBURY","500 DIRHAM/AREENA","J. FABRICS GREEN",
        "YAQOOB TEX","DYNASTY","J. FABRICS BLACK","RAJA FABIRCS","AESTHETIC GEN","ZED COURIER",
        "MT RUSK","SMILE FINE TISSUE","COSMETICS CITY","KHYBER MEDICAL","K-JUNCTION","RIDER",
        "JAZMIN","ANEELA'S","LUXURY SOFT","GRG","UPS","HIGH CLASS FABRICS","ARAMEX","ASIM JOFA",
        "BOURAQ EXPRESS","TULIP","TELEBRAND EXPRESS","ZURAJ","ELEGANCIA","ZAIB BY NIMSAY",
        "AJWA","CHASE VALUE","BAGALLERY","ACCOUTR","BODY & BLAST","TRIMCO","UNIVERSAL",
        "O-TWO-O","MASTER","MEJI RUSH","FASHION WEEK","RAJA FASHION","LEZAAR VELOOR",
        "POLKA DOT SOLVE TO GET 5% DISCOUNT","MOHSIN RASHID","RALVIL TEN",
    ],
    "printed_film": [
        "PE 2 LAYER WHITE/GREY","PE MILKY","PE NATURAL","PP","HD MILKY","PE BLACK","BOPP","PET",
        "M-PET","BOPP HOLO","HD PURE","BOPP RAINBOW","HD","PE PINK","CPP","PAPER","MATT BOPP",
        "PIVA","EVA","NON WOVEN","PE 2 LAYER NATURAL/MILKY","PE","PE 2 LAYER WHITE/BLACK",
        "PE 2 LAYER NATURAL/BLACK","EVA MATT",
    ],
    "supplier": [
        "SUBHAN","ZOHAIB","OLEFINS","MACPAC","NOVATEX","AHMED HD","G-PAK","SHABBIR PP",
        "U-FILER","AFIL FODS","BOPP","MUNDIA EXPORT","SALMAN BWANI","CHWALA CORP","ZMC",
    ],
}

# Field keys in extracted data that map to lookup categories
FIELD_LOOKUP_MAP = {
    "job_name":  "job_name",
    "material":  "printed_film",   # actual field key used in FlexoPrintingRecord
    "supplier":  "supplier",       # actual field key used in FlexoPrintingRecord
}

AUTO_CORRECT_THRESHOLD = 85   # ≥ this → silently overwrite
SUGGEST_THRESHOLD      = 60   # ≥ this → flag but still correct


def _get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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

Rules:
- Extract exactly what is written, do not calculate or infer values
- For numbers, return numeric values without units
- For dates: look for a field labeled 'Date' or 'Print Date'.
  The date is typically handwritten in DD/MM/YYYY or DD-MM-YYYY format.
  Return it exactly as written (e.g. "18/02/{current_year}").
  If the year part looks wrong or unreadable, replace it with {current_year}.
- For "material": find the cell labeled "Printed Film" in the mid-form row alongside Web Size/Web Mic.
  It contains a film type such as "PE 2 layer white/grey", "PE Milky", "BOPP", "PP", etc.
- For "plain_waste": find the cell labeled "Plain Waste" in the BOTTOM summary section. Return as a number.
- For "printed_waste": find "Printed Waste" in the BOTTOM summary section. Return as a number.
  A dash or blank means 0.
- For "plain_roll_wt": find "Plain G.wt" in the bottom summary section. Return as a number.
- For "net_wt": find "Plain Net Wt." in the bottom summary section. Return as a number.
- For "core_wt": find "Core Wt. A" in the mid-form table. Return as a number.
- For illegible handwriting, use null
- Do not add any explanation outside the JSON"""


def _encode_image(image_path: str):
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
    Apply fuzzy matching to lookup fields.
    Returns (corrected_data, corrections_log).
    corrections_log: {field: {original, corrected, score, auto}}
    """
    corrected = dict(extracted)
    log = {}

    for field_key, lookup_key in FIELD_LOOKUP_MAP.items():
        raw = corrected.get(field_key)
        if not raw or not isinstance(raw, str):
            continue

        candidates = LOOKUP[lookup_key]
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


def identify_form(image_path: str) -> dict:
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
    try:
        id_result = identify_form(image_path)
        form_code = id_result.get("form_code", "UNKNOWN")
        confidence = id_result.get("confidence", 0.0)

        matched_form = next((ft for ft in form_types if ft.code == form_code), None)
        if not matched_form:
            return {"form_code": form_code, "form_type_id": None, "data": {},
                    "confidence": confidence, "error": f"Could not match form code '{form_code}'."}

        extracted = extract_fields(image_path, matched_form)

        # Fix date year
        for date_key in ("date", "print_date"):
            if extracted.get(date_key):
                extracted[date_key] = _fix_date_year(str(extracted[date_key]))

        # Fuzzy-correct lookup fields
        corrected, corrections = _fuzzy_correct(extracted)

        return {
            "form_code": form_code,
            "form_type_id": matched_form.id,
            "data": corrected,
            "raw_data": extracted,          # original before correction
            "corrections": corrections,     # audit log for UI display
            "confidence": confidence,
            "error": None,
        }

    except json.JSONDecodeError as e:
        return {"form_code": None, "form_type_id": None, "data": {}, "confidence": 0.0,
                "error": f"JSON parse error: {str(e)}"}
    except Exception as e:
        return {"form_code": None, "form_type_id": None, "data": {}, "confidence": 0.0,
                "error": str(e)}