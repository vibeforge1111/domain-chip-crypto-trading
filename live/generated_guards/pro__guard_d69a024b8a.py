def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long: require bullish crossover (stoch_k > stoch_d) with oversold context
    if prediction == "long":
        if stoch_k > 30 or stoch_d > 30:
            return "skip"
        if stoch_k <= stoch_d:
            return "skip"
        return prediction
    
    # Short: require bearish crossover (stoch_k < stoch_d) with overbought context
    if prediction == "short":
        if stoch_k < 70 or stoch_d < 70:
            return "skip"
        if stoch_k >= stoch_d:
            return "skip"
        return prediction
    
    return prediction