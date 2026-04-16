def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using obv_slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when volume flowing out (negative obv) and momentum not oversold
    if prediction == "long" and obv_slope < -0.01 and stoch_k > 30:
        if rsi_2h < 60:
            return "skip"
    
    # Skip shorts when volume flowing in (positive obv) and momentum not overbought
    if prediction == "short" and obv_slope > 0.01 and stoch_k < 70:
        if rsi_2h > 40:
            return "skip"
    
    return prediction