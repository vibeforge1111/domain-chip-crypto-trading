def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long when OBV declining (distribution pressure)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip short when OBV rising (accumulation pressure)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction