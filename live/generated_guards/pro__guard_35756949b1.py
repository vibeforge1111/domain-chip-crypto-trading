def guard(features: dict, prediction: str) -> str:
    """Skip trades that go against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope negative (volume distribution)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope positive (volume accumulation)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction