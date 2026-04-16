def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover momentum alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct = features.get('bb_pct_b', 0.5)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # Reject if stoch_k not above stoch_d (no bullish momentum)
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if extended into overbought territory
        if stoch_k > 80 and stoch_d > 80:
            return 'skip'
        # Reject if both in oversold (exhausted bounce)
        if stoch_k < 20 and stoch_d < 20:
            return 'skip'
        # Prefer entries near lower/middle band with price above VWAP
        if bb_pct < 0.1 and vwap_dev < 0:
            return 'skip'
        # Higher timeframe alignment for longs
        if rsi_2h < 35:
            return 'skip'
            
    elif prediction == 'short':
        # Reject if stoch_k not below stoch_d (no bearish momentum)
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if extended into oversold territory
        if stoch_k < 20 and stoch_d < 20:
            return 'skip'
        # Reject if both in overbought (exhausted dump)
        if stoch_k > 80 and stoch_d > 80:
            return 'skip'
        # Prefer entries near upper band with price below VWAP
        if bb_pct > 0.9 and vwap_dev > 0:
            return 'skip'
        # Higher timeframe alignment for shorts
        if rsi_2h > 65:
            return 'skip'
    
    return prediction