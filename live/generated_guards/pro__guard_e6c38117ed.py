def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration before entry."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect momentum deceleration for long entries
    if prediction == 'long':
        # Reject if MACD histogram shows fading bullish momentum
        if macd_hist < -0.0003:
            return 'skip'
        # Reject if stochastic rolling over in overbought zone
        if stoch_k > 75 and stoch_d < stoch_k:
            return 'skip'
        # Reject if 2H RSI signals exhaustion
        if rsi_2h > 68:
            return 'skip'
    
    # Detect momentum deceleration for short entries
    elif prediction == 'short':
        if macd_hist > 0.0003:
            return 'skip'
        if stoch_k < 25 and stoch_d > stoch_k:
            return 'skip'
        if rsi_2h < 32:
            return 'skip'
    
    return prediction