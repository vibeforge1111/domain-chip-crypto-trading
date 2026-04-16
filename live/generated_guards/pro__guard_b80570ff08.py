def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_histogram = features.get('macd_histogram', 0)
    
    # High-confidence entry only at BB extremes
    if bb_pct_b < 0.05:
        # Lower band: allow longs, reject shorts
        if prediction == 'short':
            return 'skip'
    elif bb_pct_b > 0.95:
        # Upper band: allow shorts, reject longs
        if prediction == 'long':
            return 'skip'
    else:
        # Not at extreme BB zone - skip
        return 'skip'
    
    # Additional confirmation: reject if 2h RSI contradicts
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'
    
    return prediction