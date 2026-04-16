def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    
    # Skip longs when OBV is declining (distribution pressure)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation pressure)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction