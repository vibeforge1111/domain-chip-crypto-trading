def guard(features: dict, prediction: str) -> str:
    """Reject signals at overbought/oversold extremes confirmed by BB and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Overbought: BB upper band + Stochastic confirmation (>85)
    overbought = bb_pct_b > 0.88 and stoch_k > 85 and stoch_d > 80
    
    # Oversold: BB lower band + Stochastic confirmation (<15)
    oversold = bb_pct_b < 0.12 and stoch_k < 15 and stoch_d < 20
    
    # Reject longs at overbought extremes, shorts at oversold extremes
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction