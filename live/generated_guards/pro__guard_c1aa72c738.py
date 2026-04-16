def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with overbought/oversold zones."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Require stoch_k above stoch_d for longs (bullish crossover)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require stoch_k below stoch_d for shorts (bearish crossover)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Skip long entries when stoch is in overbought territory (>80)
    if prediction == "long" and stoch_k > 80:
        return "skip"
    
    # Skip short entries when stoch is in oversold territory (<20)
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction