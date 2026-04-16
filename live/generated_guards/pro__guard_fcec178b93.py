def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV flow direction."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip long trades when OBV is declining (volume outflow)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip short trades when OBV is rising (volume inflow)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction