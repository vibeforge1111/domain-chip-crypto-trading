def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope negative (distribution/volume outflow)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope positive (accumulation/volume inflow)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction