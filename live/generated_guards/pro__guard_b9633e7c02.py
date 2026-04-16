def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs during distribution (negative OBV slope)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts during accumulation (positive OBV slope)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Additional confirmation: skip longs if stoch overbought on 2h
    if prediction == "long" and rsi_2h > 65 and stoch_k > 80:
        return "skip"
    
    return prediction