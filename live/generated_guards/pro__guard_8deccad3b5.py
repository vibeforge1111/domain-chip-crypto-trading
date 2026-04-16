def guard(features: dict, prediction: str) -> str:
    """Skip trades that go against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs if OBV is declining (volume distribution)
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    
    # Skip shorts if OBV is rising (volume accumulation)
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    
    return prediction