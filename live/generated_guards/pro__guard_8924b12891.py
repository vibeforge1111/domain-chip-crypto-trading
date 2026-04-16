def guard(features: dict, prediction: str) -> str:
    """Use BB% extremes (<0.05 or >0.95) as high-confidence entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        if bb_pct_b > 0.05:
            return 'skip'
        if rsi_2h > 45 and stoch_k > 25:
            return 'skip'
    
    if prediction == 'short':
        if bb_pct_b < 0.95:
            return 'skip'
        if rsi_2h < 55 and stoch_k < 75:
            return 'skip'
    
    return prediction