def guard(features: dict, prediction: str) -> str:
    """Filter trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip longs when OBV shows distribution (smart money selling)
    if prediction == "long" and obv_slope < -0.005:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (smart money buying)
    if prediction == "short" and obv_slope > 0.005:
        return "skip"
    
    # Additional filter: overbought/oversold extreme with bad OBV alignment
    if prediction == "long" and stoch_k > 75 and obv_slope < 0:
        return "skip"
    
    if prediction == "short" and stoch_k < 25 and obv_slope > 0:
        return "skip"
    
    return prediction