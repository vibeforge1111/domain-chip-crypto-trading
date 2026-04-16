def guard(features: dict, prediction: str) -> str:
    """Detect overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long signals at overbought extremes are reversal traps
    if prediction == 'long' and bb_pct_b > 0.9 and stoch_k > 80:
        return 'skip'
    
    # Short signals at oversold extremes mean further downside is unlikely
    if prediction == 'short' and bb_pct_b < 0.1 and stoch_k < 20:
        return 'skip'
    
    return prediction