def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction (OBV slope)."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long signals when OBV shows distribution (selling pressure)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip short signals when OBV shows accumulation (buying pressure)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction