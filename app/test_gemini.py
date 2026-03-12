"""
test_gemini.py
Run from project root: python test_gemini.py <image_path>
Tests both gemini-2.0-flash and gemini-1.5-flash vision extraction.
"""
import sys
import base64
import os
import json

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
    sys.exit(1)

PROMPT = """Extract text from this image. Return a JSON object with every field and value you can read.
Return ONLY valid JSON, no explanation."""

MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]


def test_gemini(image_path: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment.")
        sys.exit(1)

    genai.configure(api_key=api_key)

    ext = image_path.rsplit(".", 1)[-1].lower()
    media_type_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    media_type = media_type_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_data = f.read()

    image_part = {"mime_type": media_type, "data": image_data}

    for model_name in MODELS:
        print(f"\n{'='*50}")
        print(f"Testing: {model_name}")
        print('='*50)
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([image_part, PROMPT])
            text = response.text.strip()
            print("Raw response:")
            print(text)

            # Try parsing as JSON
            clean = text
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            parsed = json.loads(clean.strip())
            print("\nParsed JSON OK:")
            print(json.dumps(parsed, indent=2))
        except Exception as e:
            print(f"FAILED: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_gemini.py <path_to_image>")
        sys.exit(1)
    test_gemini(sys.argv[1])