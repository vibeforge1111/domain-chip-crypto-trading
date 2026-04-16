def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Long only valid if stoch_k > stoch_d (bullish crossover)
        # Reject if stoch_k below stoch_d (bearish alignment)
        if stoch_k <= stoch_d:
            return "skip"
        # Reject if extreme overbought (>80) as reversal risk is high
        if stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Short only valid if stoch_k < stoch_d (bearish crossover)
        # Reject if stoch_k above stoch_d (bullish alignment)
        if stoch_k >= stoch_d:
            return "skip"
        # Reject if extreme oversold (<20) as reversal risk is high
        if stoch_k < 20:
            return "skip"
    
    return prediction