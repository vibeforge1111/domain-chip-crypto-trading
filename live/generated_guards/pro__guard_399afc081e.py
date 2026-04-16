def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require bullish stochastic alignment for longs
    if prediction == 'long' and stoch_k < stoch_d:
        return "skip"
    # Require bearish stochastic alignment for shorts
    if prediction == 'short' and stoch_k > stoch_d:
        return "skip"
    
    return prediction