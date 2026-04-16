def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    macd_hist = features.get('macd_histogram', 0)
    
    if prediction == 'long':
        # Reject if not in oversold extreme zone or conflicting momentum
        if bb_pct_b > 0.12:
            return 'skip'
        if stoch_k > 25 or stoch_d > 30:
            return 'skip'
        if vwap_dev > 0.008 and macd_hist < 0:
            return 'skip'
    
    if prediction == 'short':
        # Reject if not in overbought extreme zone or conflicting momentum
        if bb_pct_b < 0.88:
            return 'skip'
        if stoch_k < 75 or stoch_d > 80:
            return 'skip'
        if vwap_dev < -0.008 and macd_hist > 0:
            return 'skip'
    
    return prediction