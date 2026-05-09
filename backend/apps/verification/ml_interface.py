import json
import logging
import mimetypes
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-2.5-flash"


def _get_client():
    from google import genai
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _image_part(image_path: str):
    from google.genai import types
    mime = mimetypes.guess_type(image_path)[0] or 'image/jpeg'
    with open(image_path, 'rb') as f:
        data = f.read()
    return types.Part.from_bytes(data=data, mime_type=mime)


def _safe_json_parse(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error("[Gemini] JSON parse failed: %s", text[:200])
        return {}


def _mock_damage():
    return {"damage_detected": True, "damage_type": "tear",
            "severity": "high", "confidence": 0.85,
            "reason": "Mock fallback"}


def _mock_authentic():
    return {"is_authentic": True, "confidence": 0.90,
            "flags": [], "reason": "Mock fallback"}


def _mock_match():
    return {"is_same_product": True, "similarity_score": 0.85,
            "matched_attributes": ["category"],
            "mismatched_attributes": [], "reason": "Mock fallback"}


def detect_damage(image_path: str) -> dict:
    print(f"\n========== DETECT_DAMAGE CALLED ==========")
    print(f"[DEBUG] Image path: {image_path}")
    print(f"[DEBUG] GEMINI_API_KEY present: {bool(settings.GEMINI_API_KEY)}")
    print(f"[DEBUG] Key length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")
    print(f"[DEBUG] Key prefix: {settings.GEMINI_API_KEY[:8] if settings.GEMINI_API_KEY else 'MISSING'}")
    print(f"[DEBUG] Model name: {MODEL_NAME}")

    if not settings.GEMINI_API_KEY:
        print("[DEBUG] No API key — returning mock")
        return _mock_damage()
    try:
        client = _get_client()
        prompt = (
            "Analyze this clothing item for damage. "
            "Look for: tears, holes, rips, stains, discoloration, fading, "
            "loose threads, fabric pilling, broken zippers, missing buttons.\n\n"
            "Reply ONLY with valid JSON:\n"
            '{"damage_detected": true or false, '
            '"damage_type": "tear" or "stain" or "hole" or "discoloration" or "none", '
            '"severity": "low" or "medium" or "high", '
            '"confidence": float 0 to 1, '
            '"reason": "one sentence"}'
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, _image_part(image_path)],
        )
        print(f"[DEBUG] Raw Gemini response: {response.text}")
        result = _safe_json_parse(response.text)
        print(f"[DEBUG] Parsed result: {result}")
        if not result:
            return _mock_damage()
        final = {
            "damage_detected": result.get("damage_detected", False),
            "damage_type": result.get("damage_type", "none"),
            "severity": result.get("severity", "low"),
            "confidence": float(result.get("confidence", 0.5)),
            "reason": result.get("reason", ""),
        }
        print(f"[DEBUG] Returning damage: {final}")
        return final
    except Exception as e:
        import traceback
        print(f"[DEBUG] EXCEPTION: {e}")
        print(traceback.format_exc())
        return _mock_damage()


def check_authentic(image_path: str) -> dict:
    print(f"\n========== CHECK_AUTHENTIC CALLED ==========")
    print(f"[DEBUG] Image path: {image_path}")
    print(f"[DEBUG] GEMINI_API_KEY present: {bool(settings.GEMINI_API_KEY)}")
    print(f"[DEBUG] Key length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")
    print(f"[DEBUG] Key prefix: {settings.GEMINI_API_KEY[:8] if settings.GEMINI_API_KEY else 'MISSING'}")
    print(f"[DEBUG] Model name: {MODEL_NAME}")

    if not settings.GEMINI_API_KEY:
        print("[DEBUG] No API key — returning mock")
        return _mock_authentic()
    try:
        client = _get_client()
        prompt = (
            "Analyze this image for authenticity. "
            "Determine if it is: a real photograph, AI-generated "
            "(Midjourney/DALL-E/SD/etc.), digitally edited, a screenshot, "
            "or a stock photo from the internet.\n\n"
            "Reply ONLY with JSON:\n"
            '{"is_authentic": true or false, '
            '"confidence": float 0 to 1, '
            '"flags": ["ai_generated"] or ["edited"] or ["screenshot"] or [], '
            '"reason": "one sentence"}'
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, _image_part(image_path)],
        )
        print(f"[DEBUG] Raw Gemini response: {response.text}")
        result = _safe_json_parse(response.text)
        print(f"[DEBUG] Parsed result: {result}")
        if not result:
            return _mock_authentic()
        final = {
            "is_authentic": result.get("is_authentic", True),
            "confidence": float(result.get("confidence", 0.5)),
            "flags": result.get("flags", []),
            "reason": result.get("reason", ""),
        }
        print(f"[DEBUG] Returning authentic: {final}")
        return final
    except Exception as e:
        import traceback
        print(f"[DEBUG] EXCEPTION: {e}")
        print(traceback.format_exc())
        return _mock_authentic()


def match_product(damage_image_path: str, order) -> dict:
    print(f"\n========== MATCH_PRODUCT CALLED ==========")
    print(f"[DEBUG] Image path: {damage_image_path}")
    print(f"[DEBUG] GEMINI_API_KEY present: {bool(settings.GEMINI_API_KEY)}")
    print(f"[DEBUG] Key length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")
    print(f"[DEBUG] Key prefix: {settings.GEMINI_API_KEY[:8] if settings.GEMINI_API_KEY else 'MISSING'}")
    print(f"[DEBUG] Model name: {MODEL_NAME}")

    if not settings.GEMINI_API_KEY:
        print("[DEBUG] No API key — returning mock")
        return _mock_match()
    try:
        first_item = order.items.first()
        if not first_item:
            return {"is_same_product": False, "similarity_score": 0.0,
                    "matched_attributes": [],
                    "mismatched_attributes": ["no_items"],
                    "reason": "Order has no items"}

        product_color = first_item.color or "unknown"
        product_size = first_item.size or "unknown"
        category = (
            first_item.product.category.name
            if first_item.product and first_item.product.category
            else "clothing"
        )

        has_ref = False
        ref_part = None
        try:
            if first_item.product_image:
                ref_path = Path(settings.MEDIA_ROOT) / str(first_item.product_image)
                if ref_path.exists():
                    ref_part = _image_part(str(ref_path))
                    has_ref = True
        except Exception as e:
            logger.warning("[Gemini] No ref image: %s", e)

        prompt = (
            "You are verifying a clothing replacement claim. "
            "The customer is claiming their received item arrived damaged.\n\n"
            f"CUSTOMER ORDERED:\n"
            f"- Category: {category}\n"
            f"- Color: {product_color}\n"
            f"- Size: {product_size}\n\n"
            "The submitted photo shows the DAMAGED item — it will have tears, holes, stains, "
            "or other defects. DO NOT penalise for damage when comparing.\n\n"
            "Focus ONLY on these base characteristics despite the damage:\n"
            "1. Is it the same category of clothing (e.g. t-shirt, shirt, trousers)?\n"
            "2. Is the base color broadly similar?\n"
            "3. Is the basic silhouette/cut similar?\n\n"
            "Be LENIENT — a heavily torn item still matches if category and color align. "
            "Only return false if it is clearly a completely different garment type or color.\n\n"
            + ("A reference product photo is also attached. " if has_ref else "")
            + "Reply ONLY with JSON:\n"
            '{"is_same_product": true or false, '
            '"similarity_score": float 0 to 1, '
            '"matched_attributes": ["color","category","shape"], '
            '"mismatched_attributes": [], '
            '"reason": "one sentence"}'
        )

        contents = [prompt, _image_part(damage_image_path)]
        if ref_part:
            contents.append(ref_part)

        client = _get_client()
        response = client.models.generate_content(model=MODEL_NAME, contents=contents)
        print(f"[DEBUG] Raw Gemini response: {response.text}")
        result = _safe_json_parse(response.text)
        print(f"[DEBUG] Parsed result: {result}")
        if not result:
            return _mock_match()
        final = {
            "is_same_product": result.get("is_same_product", True),
            "similarity_score": float(result.get("similarity_score", 0.5)),
            "matched_attributes": result.get("matched_attributes", []),
            "mismatched_attributes": result.get("mismatched_attributes", []),
            "reason": result.get("reason", ""),
        }
        print(f"[DEBUG] Returning match: {final}")
        return final
    except Exception as e:
        import traceback
        print(f"[DEBUG] EXCEPTION: {e}")
        print(traceback.format_exc())
        return _mock_match()
