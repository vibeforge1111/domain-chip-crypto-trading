def guard(features: dict, prediction: str) -> str:
    """Custom guard function using stochastic crossover for entry timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_d > 35:
            return "skip"
        if vwap_dev < -0.005:
            return "skip"
    
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_d < 65:
            return "skip"
        if vwap_dev > 0.005:
            return "skip"
    
    return prediction