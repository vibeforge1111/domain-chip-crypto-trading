def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Detect crossover: k crosses above d = bullish, below = bearish
    if stoch_k > stoch_d and stoch_d < 30:
        return prediction  # bullish crossover - allow longs
    if stoch_k < stoch_d and stoch_d > 70:
        return prediction  # bearish crossover - allow shorts
    
    # No crossover: verify momentum alignment
    if prediction == 'long':
        if stoch_k <= stoch_d or stoch_d >= 30 or vwap_dev <= 0:
            return 'skip'
    elif prediction == 'short':
        if stoch_k >= stoch_d or stoch_d <= 70 or vwap_dev >= 0:
            return 'skip'
    
    return prediction