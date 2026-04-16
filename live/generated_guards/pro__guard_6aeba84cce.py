def guard(features: dict, prediction: str) -> str:
    """Skip trades where OBV slope contradicts prediction direction."""
    obv_slope = features.get('obv_slope', 0)
    
    # Skip longs when OBV flow is strongly negative (distribution)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV flow is strongly positive (accumulation)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction