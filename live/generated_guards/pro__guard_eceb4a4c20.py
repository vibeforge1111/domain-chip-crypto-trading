def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Only filter when volume is above average (trustworthy OBV signal)
    if volume_ratio < 1.2:
        return prediction
    
    # Skip longs when OBV is falling (distribution - bearish volume)
    if prediction == 'long' and obv_slope < -0.1:
        return 'skip'
    
    # Skip shorts when OBV is rising (accumulation - bullish volume)
    if prediction == 'short' and obv_slope > 0.1:
        return 'skip'
    
    return prediction