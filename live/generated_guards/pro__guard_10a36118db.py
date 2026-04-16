def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require meaningful crossover separation
    if abs(stoch_k - stoch_d) < 5:
        return "skip"
    
    # Long: stoch_k above stoch_d AND in/just-leaving oversold zone
    if prediction == "long" and stoch_k > stoch_d:
        if stoch_k <= 40:
            return prediction
        return "skip"
    
    # Short: stoch_k below stoch_d AND in/just-leaving overbought zone
    if prediction == "short" and stoch_k < stoch_d:
        if stoch_k >= 60:
            return prediction
        return "skip"
    
    return "skip"