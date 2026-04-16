def guard(features: dict, prediction: str) -> str:
    """Reject trades in choppy/extended conditions without volume confirmation."""
    bb_position = features.get("bb_position", 0.5)
    volume_ratio = features.get("volume_ratio", 1.0)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Reject if price is near band extremes (extended) with weak volume and poor structure
    is_extended = bb_position < 0.15 or bb_position > 0.85
    low_volume = volume_ratio < 0.8
    weak_body = body_ratio < 0.3
    
    if is_extended and low_volume and weak_body:
        return "skip"
    
    return prediction