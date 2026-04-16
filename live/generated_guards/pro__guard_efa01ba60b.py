def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Require clear crossover: stoch_k must be on opposite side of stoch_d
    if abs(stoch_k - stoch_d) < 5:
        return "skip"
    
    # Long signals need stoch_k below stoch_d (bullish crossover setup) and oversold
    if prediction == "long":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k > 30:  # Not oversold enough
            return "skip"
        if rsi_2h < 40:  # Wider timeframe confirming oversold
            return "skip"
    
    # Short signals need stoch_k above stoch_d (bearish crossover setup) and overbought
    if prediction == "short":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k < 70:  # Not overbought enough
            return "skip"
        if rsi_2h > 60:  # Wider timeframe confirming overbought
            return "skip"
    
    return prediction