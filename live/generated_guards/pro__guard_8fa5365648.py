def guard(features: dict, prediction: str) -> str:
    """Filter trades where candle rejection exceeds conviction."""
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    
    # High wick = candle rejected at that level, reject if volume confirms weakness
    if total_wick > 0.55 and features.get('volume_ratio', 1) < 0.75:
        return "skip"
    
    return prediction