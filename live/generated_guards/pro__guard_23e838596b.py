def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == 'long':
        # Require bullish stochastic alignment (k above d) with room to run
        if stoch_k <= stoch_d or stoch_k < 30 or stoch_k > 70:
            return 'skip'
        # Confirm with 2h RSI not bearish
        if rsi_2h < 40:
            return 'skip'
        # Volume confirmation
        if obv_slope < 0:
            return 'skip'
    
    elif prediction == 'short':
        # Require bearish stochastic alignment (k below d) with room to run
        if stoch_k >= stoch_d or stoch_k > 70 or stoch_k < 30:
            return 'skip'
        # Confirm with 2h RSI not bullish
        if rsi_2h > 60:
            return 'skip'
        # Volume confirmation
        if obv_slope > 0:
            return 'skip'
    
    return prediction