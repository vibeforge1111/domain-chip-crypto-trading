def guard(features: dict, prediction: str) -> str:
    """Guard using BB extreme zones with stochastic confirmation."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_hist = features.get("macd_histogram", 0)
    
    if prediction == "long":
        if bb_pct >= 0.05 or stoch_k >= 20 or stoch_d <= 50:
            return "skip"
    elif prediction == "short":
        if bb_pct <= 0.95 or stoch_k <= 80 or stoch_d >= 50:
            return "skip"
    
    return prediction