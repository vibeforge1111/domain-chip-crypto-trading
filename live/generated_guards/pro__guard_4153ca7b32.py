def guard(features: dict, prediction: str) -> str:
    """Guard using stoch_k vs stoch_d crossover for precise entry timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # For long: stoch_k should be above stoch_d after pullback into oversold
    if prediction == "long":
        if stoch_d > 25 or stoch_k <= stoch_d:
            return "skip"
    
    # For short: stoch_k should be below stoch_d after rally into overbought
    elif prediction == "short":
        if stoch_d < 75 or stoch_k >= stoch_d:
            return "skip"
    
    # Require VWAP alignment
    if prediction == "long" and vwap_deviation < -0.002:
        return "skip"
    if prediction == "short" and vwap_deviation > 0.002:
        return "skip"
    
    return prediction