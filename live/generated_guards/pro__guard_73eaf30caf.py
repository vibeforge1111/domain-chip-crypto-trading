def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow as indicated by OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Skip longs when OBV slope is negative (distribution/weak volume)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope is positive (accumulation/strong volume)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction