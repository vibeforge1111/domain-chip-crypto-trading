def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction with VWAP confirmation."""
    if prediction == "skip":
        return prediction
    
    obv = features.get("obv_slope", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip longs when OBV is negative and price below VWAP (smart money distributing)
    if prediction == "long" and obv < -0.2 and vwap_dev < 0:
        return "skip"
    
    # Skip shorts when OBV is positive and price above VWAP (smart money accumulating)
    if prediction == "short" and obv > 0.2 and vwap_dev > 0:
        return "skip"
    
    return prediction