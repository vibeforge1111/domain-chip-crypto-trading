def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Require stochastic alignment with prediction direction
    if prediction == 'long':
        if stoch_k < stoch_d - 5:  # bearish crossover zone
            return 'skip'
    elif prediction == 'short':
        if stoch_k > stoch_d + 5:  # bullish crossover zone
            return 'skip'
    
    # Additional confirmation: check vwap alignment
    if prediction == 'long' and vwap_dev < -0.005:
        # Price well below VWAP, skip long
        return 'skip'
    if prediction == 'short' and vwap_dev > 0.005:
        # Price well above VWAP, skip short
        return 'skip'
    
    return prediction