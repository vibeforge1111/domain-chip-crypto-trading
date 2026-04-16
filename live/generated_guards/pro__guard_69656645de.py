def guard(features: dict, prediction: str) -> str:
    """Filter signals at overbought/oversold extremes using BB position and stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long when overbought on multiple indicators
    if prediction == 'long' and stoch_k > 80 and bb_pct_b > 0.85:
        return 'skip'
    
    # Skip short when oversold on multiple indicators
    if prediction == 'short' and stoch_k < 20 and bb_pct_b < 0.15:
        return 'skip'
    
    return prediction