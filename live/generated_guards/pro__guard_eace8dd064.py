def guard(features: dict, prediction: str) -> str:
    """Skip trades that go against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction