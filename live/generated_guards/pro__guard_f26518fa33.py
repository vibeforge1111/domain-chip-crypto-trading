def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV flow direction."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs when OBV declining (smart money distributing)
    if prediction == "long" and obv_slope < -0.05 and stoch_k > 65:
        return "skip"
    
    # Skip shorts when OBV rising (smart money accumulating)
    if prediction == "short" and obv_slope > 0.05 and stoch_k < 35:
        return "skip"
    
    return prediction