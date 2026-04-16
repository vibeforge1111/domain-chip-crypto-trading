def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Filter: disagreement between vwap_deviation and momentum
    if vwap_dev > 0.003 and momentum < -0.05:
        return "skip"
    if vwap_dev < -0.003 and momentum > 0.05:
        return "skip"
    
    # Filter: stochastic extremes conflict with 2h RSI direction
    if prediction == "long" and stoch_k > 85 and rsi_2h < 40:
        return "skip"
    if prediction == "short" and stoch_k < 15 and rsi_2h > 60:
        return "skip"
    
    return prediction