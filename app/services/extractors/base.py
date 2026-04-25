"""
extractors/base.py
Shared utilities used by all form-specific extractors.
"""
import os
import json
import base64
from datetime import datetime
from openai import OpenAI
from rapidfuzz import process, fuzz

try:
    from app.services.lookup_tables import LOOKUP_TABLES
    LOOKUP = LOOKUP_TABLES
except ImportError:
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
            "O-TWO-O", "POLKA DOT", "POLKA DOT SALE", "RAJA FABIRCS", "RAJA FASHION",
            "RALVIL TEN", "RIDER", "RONIN", "SADAR APP", "SHOP REX", "SKY NET",
            "SMILE FINE TISSUE", "STITCHER", "TELEBRAND EXPRESS", "TOUHEED/HAQ HALAL",
            "TRIMCO", "TULIP", "UNIVERSAL", "UPS", "YAQOOB TEX", "ZAIB BY NIMSAY",
            "ZARPOSH", "ZED COURIER", "ZELLBURY", "ZURAJ",
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

AUTO_CORRECT_THRESHOLD = 85
SUGGEST_THRESHOLD = 60


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path: str) -> tuple[str, str]:
    ext = image_path.rsplit(".", 1)[-1].lower()
    media_type = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "webp": "image/webp", "gif": "image/gif",
    }.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def fix_date_year(value: str) -> str:
    if not value:
        return value
    current_year = datetime.now().year
    for sep in ("/", "-"):
        parts = value.split(sep)
        if len(parts) == 3:
            year_part = parts[2].strip()
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


def fuzzy_correct(extracted: dict, field_lookup_map: dict) -> tuple[dict, dict]:
    corrected = dict(extracted)
    log = {}
    for field_key, lookup_key in field_lookup_map.items():
        raw = corrected.get(field_key)
        if not raw or not isinstance(raw, str):
            continue
        candidates = LOOKUP.get(lookup_key, [])
        if not candidates:
            continue
        scorer = fuzz.partial_ratio if len(raw) <= 6 else fuzz.token_sort_ratio
        match, score, _ = process.extractOne(
            raw.upper(), [c.upper() for c in candidates], scorer=scorer
        )
        best = candidates[[c.upper() for c in candidates].index(match)]
        if score >= SUGGEST_THRESHOLD and best.upper() != raw.upper():
            log[field_key] = {"original": raw, "corrected": best, "score": score, "auto": True}
            corrected[field_key] = best
    return corrected, log


def validate_against_lookup(data: dict, field_lookup_map: dict) -> dict:
    flags = {}
    for field_key, lookup_key in field_lookup_map.items():
        value = data.get(field_key)
        if not value or not isinstance(value, str):
            flags[field_key] = True
            continue
        candidates = LOOKUP.get(lookup_key, [])
        flags[field_key] = any(value.upper() == c.upper() for c in candidates) if candidates else True
    return flags


def validate_waste_totals(data: dict) -> dict:
    waste_fields = ["plain_waste", "roll_waste", "printed_waste", "setting_waste"]
    numeric_parts = [float(data[f]) for f in waste_fields if data.get(f) is not None]
    if not numeric_parts:
        return data
    computed = round(sum(numeric_parts), 3)
    extracted_total = data.get("total_waste")
    if extracted_total is None:
        data["total_waste"] = computed
        return data
    try:
        extracted_total = float(extracted_total)
    except (TypeError, ValueError):
        data["total_waste"] = computed
        return data
    tolerance = max(0.05, computed * 0.05)
    if abs(extracted_total - computed) > tolerance:
        data["total_waste"] = computed
    return data


def vision_call(image_path: str, prompt: str, max_tokens: int = 256, detail: str = "low") -> str:
    img_data, media_type = encode_image(image_path)
    response = get_client().chat.completions.create(
        model="gpt-4o",
        max_tokens=max_tokens,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {
                    "url": f"data:{media_type};base64,{img_data}", "detail": detail
                }},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return response.choices[0].message.content
