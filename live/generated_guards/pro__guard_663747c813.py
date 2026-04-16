def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    if prediction == "long":
        # Require bullish crossover (k above d)
        if stoch_k <= stoch_d:
            return "skip"
        # Avoid extreme oversold (reversal risk)
        if stoch_k < 15:
            return "skip"
        # Require minimum crossover strength
        if (stoch_k - stoch_d) < 4:
            return "skip"
        # MACD should not contradict momentum
        if macd_histogram < -0.0003:
            return "skip"
        # VWAP should not be deeply below price for longs
        if vwap_deviation < -0.015:
            return "skip"
    
    elif prediction == "short":
        # Require bearish crossover (k below d)
        if stoch_k >= stoch_d:
            return "skip"
        # Avoid extreme overbought (reversal risk)
        if stoch_k > 85:
            return "skip"
        # Require minimum crossover strength
        if (stoch_d - stoch_k) < 4:
            return "skip"
        # MACD should not contradict momentum
        if macd_histogram > 0.0003:
            return "skip"
        # VWAP should not be deeply above price for shorts
        if vwap_deviation > 0.015:
            return "skip"
    
    return prediction