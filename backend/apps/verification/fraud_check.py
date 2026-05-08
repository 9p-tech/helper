from apps.claims.models import ClaimFile


def check_duplicate_image(image_path: str, current_claim_id: str) -> dict:
    """
    Compute perceptual hash of image and compare against all previous claim files.
    Returns: {duplicate_found, duplicate_claim_id}
    """
    try:
        import imagehash
        from PIL import Image
        img_hash = str(imagehash.phash(Image.open(image_path)))
    except Exception:
        return {'duplicate_found': False, 'duplicate_claim_id': ''}

    existing = ClaimFile.objects.filter(
        file_type=ClaimFile.DAMAGE_PHOTO,
        image_hash=img_hash,
    ).exclude(claim_id=current_claim_id).first()

    if existing:
        return {'duplicate_found': True, 'duplicate_claim_id': existing.claim_id}

    ClaimFile.objects.filter(
        claim_id=current_claim_id,
        file_type=ClaimFile.DAMAGE_PHOTO
    ).update(image_hash=img_hash)

    return {'duplicate_found': False, 'duplicate_claim_id': ''}
