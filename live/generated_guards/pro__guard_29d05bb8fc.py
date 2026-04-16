def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Skip longs when volume is distributing (negative OBV slope)
    if prediction == 'long' and obv_slope < -0.1:
        return 'skip'
    
    # Skip shorts when volume is accumulating (positive OBV slope)
    if prediction == 'short' and obv_slope > 0.1:
        return 'skip'
    
    return prediction