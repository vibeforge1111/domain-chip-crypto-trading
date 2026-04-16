def guard(features: dict, prediction: str) -> str:
    """Guard using stoch_k/d crossover with zone confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long signal: stoch_k crosses above stoch_d from oversold zone
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_k > 30:  # Not in oversold, likely weak entry
            return 'skip'
    
    # Short signal: stoch_k crosses below stoch_d from overbought zone
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_k < 70:  # Not in overbought, likely weak entry
            return 'skip'
    
    return prediction