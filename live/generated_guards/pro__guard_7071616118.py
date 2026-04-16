def guard(features: dict, prediction: str) -> str:
    """Skip trades misaligned with broader 2h trend and momentum."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long":
        if rsi_2h < 45 and stoch_k < 50 and obv_slope < 0:
            return "skip"
    
    if prediction == "short":
        if rsi_2h > 55 and stoch_k > 50 and obv_slope > 0:
            return "skip"
    
    return prediction