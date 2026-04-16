def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict volume flow direction (OBV)."""
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    
    return prediction