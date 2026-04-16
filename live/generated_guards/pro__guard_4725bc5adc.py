def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Long entries need bullish stochastic crossover
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        # Reject if 2h RSI is overbought (potential reversal)
        if rsi_2h > 70:
            return "skip"
    
    # Short entries need bearish stochastic crossover
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        # Reject if 2h RSI is oversold (potential reversal)
        if rsi_2h < 30:
            return "skip"
    
    return prediction