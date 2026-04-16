def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs during distribution or shorting during accumulation
    if prediction == "long" and (obv_slope < -0.1 or rsi_2h > 70):
        return "skip"
    if prediction == "short" and (obv_slope > 0.1 or rsi_2h < 30):
        return "skip"
    
    return prediction