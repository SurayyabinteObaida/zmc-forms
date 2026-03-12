"""
extraction_service.py
Handles image-to-structured-data extraction via OpenAI Vision API.
Uses 4 GPT models in parallel with majority-vote consensus for accuracy.
"""
import os
import json
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from openai import OpenAI
from app.models import FormType


def _get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_MODELS = ["gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-mini", "gpt-4-turbo"]

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
- For dates: look carefully for a field labeled 'Date' or 'Print Date'. 
  The date is typically handwritten in DD/MM/YYYY or DD-MM-YYYY format.
  Return it exactly as written (e.g. "18/02/2026"). If only partially visible, return what is readable.
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


def _majority_vote(results: list[dict]) -> dict:
    if not results:
        return {}
    all_keys = set(k for r in results for k in r.keys())
    consensus = {}
    for key in all_keys:
        values = [r.get(key) for r in results]
        str_values = [json.dumps(v, sort_keys=True) for v in values]
        most_common_str, count = Counter(str_values).most_common(1)[0]
        if count >= 2:
            consensus[key] = json.loads(most_common_str)
        else:
            non_null = [v for v in values if v is not None]
            consensus[key] = non_null[0] if non_null else None
    return consensus


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


def _extract_with_model(model: str, image_data: str, media_type: str, prompt: str) -> dict:
    response = _get_client().chat.completions.create(
        model=model,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_data}", "detail": "high"}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return _parse_json_response(response.choices[0].message.content)


def extract_fields(image_path: str, form_type: FormType) -> dict:
    """Returns {"consensus": {...}, "model_results": {"gpt-4o": {...}, ...}}"""
    image_data, media_type = _encode_image(image_path)
    prompt = _build_extraction_prompt(form_type)

    model_results = {}
    with ThreadPoolExecutor(max_workers=len(EXTRACTION_MODELS)) as executor:
        futures = {
            executor.submit(_extract_with_model, model, image_data, media_type, prompt): model
            for model in EXTRACTION_MODELS
        }
        for future in as_completed(futures):
            model = futures[future]
            try:
                model_results[model] = future.result()
            except Exception as e:
                print(f"[extraction_service] Model {model} failed: {e}")
                model_results[model] = None

    successful = [v for v in model_results.values() if v is not None]
    if not successful:
        raise RuntimeError("All models failed during extraction.")

    consensus = _majority_vote(successful)
    return {"consensus": consensus, "model_results": model_results}


def process_image(image_path: str, form_types: list) -> dict:
    try:
        id_result = identify_form(image_path)
        form_code = id_result.get("form_code", "UNKNOWN")
        confidence = id_result.get("confidence", 0.0)

        matched_form = next((ft for ft in form_types if ft.code == form_code), None)

        if not matched_form:
            return {"form_code": form_code, "form_type_id": None, "data": {},
                    "model_results": {}, "confidence": confidence,
                    "error": f"Could not match form code '{form_code}'."}

        extracted = extract_fields(image_path, matched_form)
        return {
            "form_code": form_code,
            "form_type_id": matched_form.id,
            "data": extracted["consensus"],
            "model_results": extracted["model_results"],
            "confidence": confidence,
            "error": None,
        }

    except json.JSONDecodeError as e:
        return {"form_code": None, "form_type_id": None, "data": {}, "model_results": {},
                "confidence": 0.0, "error": f"JSON parse error: {str(e)}"}
    except Exception as e:
        return {"form_code": None, "form_type_id": None, "data": {}, "model_results": {},
                "confidence": 0.0, "error": str(e)}