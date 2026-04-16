def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extreme positions for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        if bb_pct_b >= 0.05:
            return 'skip'
        if vwap_deviation > -0.005:
            return 'skip'
        if rsi_2h < 40:
            return 'skip'
    elif prediction == 'short':
        if bb_pct_b <= 0.95:
            return 'skip'
        if vwap_deviation < 0.005:
            return 'skip'
        if rsi_2h > 60:
            return 'skip'
    
    return prediction