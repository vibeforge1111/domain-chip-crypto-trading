def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic alignment and zone timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require bullish alignment for longs (K above D)
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        # Avoid entries when already overbought
        if stoch_k > 85:
            return "skip"
    
    # Require bearish alignment for shorts (K below D)
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        # Avoid entries when already oversold
        if stoch_k < 15:
            return "skip"
    
    return prediction