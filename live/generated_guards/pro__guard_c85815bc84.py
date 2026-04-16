def guard(features: dict, prediction: str) -> str:
    """Filter trades when candle structure shows indecision with weak volume confirmation."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body = features.get('body_ratio', 0)
    volume = features.get('volume_ratio', 1)
    
    wick_sum = upper_wick + lower_wick
    # Doji-like candle (high wicks, low body)
    if wick_sum > 0.65 and body < 0.35:
        return "skip"
    
    # Dominant upper wick with low volume = rejection
    if upper_wick > 0.45 and volume < 0.8:
        return "skip"
    
    # Dominant lower wick with low volume = rejection
    if lower_wick > 0.45 and volume < 0.8:
        return "skip"
    
    return prediction