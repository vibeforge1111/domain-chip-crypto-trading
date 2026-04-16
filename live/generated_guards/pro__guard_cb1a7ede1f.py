def guard(features: dict, prediction: str) -> str:
    """Reject signals when wick dominance contradicts trend direction."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    ema_slope = features.get('ema_slope', 0)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Long signal: reject if dominant upper wick against flat/downtrend, unless volume is strong
    if upper_wick > 0.35 and ema_slope <= 0 and prediction == "long" and volume_ratio < 1.3:
        return "skip"
    
    # Short signal: reject if dominant lower wick against flat/uptrend, unless volume is strong
    if lower_wick > 0.35 and ema_slope >= 0 and prediction == "short" and volume_ratio < 1.3:
        return "skip"
    
    return prediction