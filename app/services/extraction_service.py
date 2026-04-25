"""
extraction_service.py  (V2)
Thin dispatcher. classify_image() + extract() only.
All form-specific logic lives in services/extractors/.
"""
import json
from app.models import FormType
from app.services.extractors.base import vision_call, parse_json

FORM_CODE_NAMES = {
    "F-PRD/01.2": "Flexo Printing Production Report",
    "F-PRD/01.1": "Gravure Printing Production Report",
}

_CLASSIFY_PROMPT = """You are reading a ZMC manufacturing production form.
Look ONLY at the form header — the title and form code printed at the top.

Known forms:
- F-PRD/01.2 → Flexo Printing Production Report
- F-PRD/01.1 → Gravure Printing Production Report (titled "ZMC Printing Production Report")

Respond with ONLY a JSON object, nothing else:
{
  "form_code": "F-PRD/01.2" or "F-PRD/01.1" or "UNKNOWN",
  "confidence": 0.0 to 1.0
}"""


def classify_image(image_path: str) -> dict:
    """
    Lightweight classification — reads form header only.
    Returns: {form_code, form_name, confidence, error}
    """
    try:
        raw = vision_call(image_path, _CLASSIFY_PROMPT, max_tokens=128, detail="low")
        result = parse_json(raw)
        form_code = result.get("form_code", "UNKNOWN")
        return {
            "form_code": form_code,
            "form_name": FORM_CODE_NAMES.get(form_code, "Unknown Form"),
            "confidence": float(result.get("confidence", 0.0)),
            "error": None,
        }
    except Exception as e:
        return {
            "form_code": "UNKNOWN",
            "form_name": "Unknown Form",
            "confidence": 0.0,
            "error": str(e),
        }


def extract(form_type_code: str, image_path: str, form_type_obj: FormType = None) -> dict:
    """
    Dispatch extraction to the correct form-specific extractor.
    Returns: {data, corrections, validation_flags, confidence, error}
    """
    try:
        if form_type_code == "F-PRD/01.2":
            from app.services.extractors.flexo import extract as extract_flexo
            if not form_type_obj:
                raise ValueError("form_type_obj required for Flexo extraction")
            result = extract_flexo(image_path, form_type_obj)

        elif form_type_code == "F-PRD/01.1":
            from app.services.extractors.gravure import extract as extract_gravure
            result = extract_gravure(image_path)

        else:
            return {
                "data": {}, "corrections": {}, "validation_flags": {},
                "confidence": 0.0,
                "error": f"No extractor defined for form type '{form_type_code}'.",
            }

        result["confidence"] = 1.0
        result["error"] = None
        return result

    except json.JSONDecodeError as e:
        return {"data": {}, "corrections": {}, "validation_flags": {},
                "confidence": 0.0, "error": f"JSON parse error: {e}"}
    except Exception as e:
        return {"data": {}, "corrections": {}, "validation_flags": {},
                "confidence": 0.0, "error": str(e)}
