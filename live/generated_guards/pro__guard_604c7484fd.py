def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == 'long':
        # Stochastic bullish crossover from oversold zone
        if stoch_k <= stoch_d or stoch_k > 30:
            return 'skip'
        # Wider timeframe confirmation
        if rsi_2h < 45:
            return 'skip'
        # Price should be near lower band
        if bb_pct_b > 0.25:
            return 'skip'
    
    elif prediction == 'short':
        # Stochastic bearish crossover from overbought zone
        if stoch_k >= stoch_d or stoch_k < 70:
            return 'skip'
        # Wider timeframe confirmation
        if rsi_2h > 55:
            return 'skip'
        # Price should be near upper band
        if bb_pct_b < 0.75:
            return 'skip'
    
    return prediction