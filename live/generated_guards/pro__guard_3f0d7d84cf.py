def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with zone confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # For long signals: require bullish crossover (k crosses above d) in oversold zone
    if prediction == 'long':
        if stoch_k <= stoch_d:  # No bullish crossover
            return 'skip'
        if stoch_d > 50:  # Not in favorable oversold area
            return 'skip'
        if vwap_dev > 0:  # Price above VWAP for longs is weak
            return 'skip'
    
    # For short signals: require bearish crossover (k crosses below d) in overbought zone
    elif prediction == 'short':
        if stoch_k >= stoch_d:  # No bearish crossover
            return 'skip'
        if stoch_d < 50:  # Not in favorable overbought area
            return 'skip'
        if vwap_dev < 0:  # Price below VWAP for shorts is weak
            return 'skip'
    
    return prediction