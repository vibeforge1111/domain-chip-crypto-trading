def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV shows distribution (negative) with price below VWAP
    if prediction == "long" and obv_slope < -0.05 and vwap_deviation < -0.001:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (positive) with price above VWAP
    if prediction == "short" and obv_slope > 0.05 and vwap_deviation > 0.001:
        return "skip"
    
    return prediction