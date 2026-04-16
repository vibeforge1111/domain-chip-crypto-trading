def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    
    # Skip longs when OBV is declining (volume flowing out = distribution)
    if prediction == "long" and obv_slope < -0.2:
        return "skip"
    
    # Skip shorts when OBV is rising (volume flowing in = accumulation)
    if prediction == "short" and obv_slope > 0.2:
        return "skip"
    
    return prediction