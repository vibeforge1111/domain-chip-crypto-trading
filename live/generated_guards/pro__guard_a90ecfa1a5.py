def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover momentum filter - avoid entries against weakening momentum."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Reject longs when overbought but K crossing below D (momentum fading)
    if prediction == "long" and stoch_k > 80 and stoch_k < stoch_d:
        return "skip"
    
    # Reject shorts when oversold but K crossing above D (bounce likely)
    if prediction == "short" and stoch_k < 20 and stoch_k > stoch_d:
        return "skip"
    
    return prediction