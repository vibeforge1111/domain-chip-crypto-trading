def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing precision."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    stoch_diff = stoch_k - stoch_d
    
    # For long entries: require bullish crossover (k crossed above d) in oversold zone
    if prediction == 'long':
        if stoch_diff <= 0 or stoch_k > 25:
            return "skip"
    
    # For short entries: require bearish crossover (k crossed below d) in overbought zone
    elif prediction == 'short':
        if stoch_diff >= 0 or stoch_k < 75:
            return "skip"
    
    return prediction