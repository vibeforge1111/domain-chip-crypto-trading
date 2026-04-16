def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # For long entries, require bullish stochastic alignment and not extended
    if prediction == "long":
        if stoch_k < stoch_d:
            return "skip"
        if stoch_k > 85:
            return "skip"
        if vwap_dev > 0.015:
            return "skip"
    
    # For short entries, require bearish stochastic alignment and not oversold
    if prediction == "short":
        if stoch_k > stoch_d:
            return "skip"
        if stoch_k < 15:
            return "skip"
        if vwap_dev < -0.015:
            return "skip"
    
    return prediction