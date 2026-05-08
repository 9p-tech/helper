"""
ML interface — replace mock functions with your friend's real model calls.

Expected signatures:
    detect_damage(image_path: str) -> dict
    check_authentic(image_path: str) -> dict
"""


def detect_damage(image_path: str) -> dict:
    """
    Mock implementation. Replace with actual model call.
    Returns: {damage_detected, damage_type, severity, confidence}
    """
    return {
        'damage_detected': True,
        'damage_type': 'tear',
        'severity': 'medium',
        'confidence': 0.82,
    }


def check_authentic(image_path: str) -> dict:
    """
    Mock implementation. Replace with actual model call.
    Returns: {is_authentic, confidence, flags}
    """
    return {
        'is_authentic': True,
        'confidence': 0.91,
        'flags': [],
    }
