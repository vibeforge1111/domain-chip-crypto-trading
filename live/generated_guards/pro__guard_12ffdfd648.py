def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with momentum confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_hist = features.get('macd_histogram', 0)
    
    if prediction == 'long':
        # Accept bullish crossover only in oversold with lower band proximity
        if stoch_k > stoch_d and stoch_d < 25 and bb_pct_b < 0.2:
            if macd_hist > 0:
                return prediction
        return 'skip'
    
    elif prediction == 'short':
        # Accept bearish crossover only in overbought with upper band proximity
        if stoch_k < stoch_d and stoch_d > 75 and bb_pct_b > 0.8:
            if macd_hist < 0:
                return prediction
        return 'skip'
    
    return prediction