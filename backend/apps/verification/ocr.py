import re


def extract_invoice_data(image_path: str) -> dict:
    """
    Run Tesseract OCR on an invoice image.
    Returns: {raw_text, order_id_found, date_found}
    """
    raw_text = ''
    order_id_found = ''
    date_found = ''

    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        raw_text = pytesseract.image_to_string(img)
    except Exception:
        return {'raw_text': raw_text, 'order_id_found': order_id_found, 'date_found': date_found}

    order_match = re.search(r'SN\d{6}[A-Z0-9]{4}', raw_text)
    if order_match:
        order_id_found = order_match.group(0)

    date_match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', raw_text)
    if date_match:
        date_found = date_match.group(0)

    return {
        'raw_text': raw_text,
        'order_id_found': order_id_found,
        'date_found': date_found,
    }
