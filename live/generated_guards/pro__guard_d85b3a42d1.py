def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is at Bollinger Band + Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long signals when overbought (upper BB + overbought stochastic + high RSI context)
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 85 and stoch_d > 75 and rsi_2h > 60:
        return 'skip'
    
    # Skip short signals when oversold (lower BB + oversold stochastic + low RSI context)
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 15 and stoch_d < 25 and rsi_2h < 40:
        return 'skip'
    
    return prediction