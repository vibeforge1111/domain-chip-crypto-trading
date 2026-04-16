def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Longs need bullish crossover (k crosses above d) from oversold
    if prediction == "long" and (stoch_k <= stoch_d or stoch_k > 30):
        return "skip"
    
    # Shorts need bearish crossover (k crosses below d) from overbought
    if prediction == "short" and (stoch_k >= stoch_d or stoch_k < 70):
        return "skip"
    
    return prediction