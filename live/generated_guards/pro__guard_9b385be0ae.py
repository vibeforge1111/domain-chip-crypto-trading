def guard(features: dict, prediction: str) -> str:
    """Filter trades when Bollinger Band position and Stochastic agree on extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Both indicators overbought - reject longs
    if bb_pct_b > 0.9 and stoch_k > 80 and prediction == 'long':
        return 'skip'
    
    # Both indicators oversold - reject shorts
    if bb_pct_b < 0.1 and stoch_k < 20 and prediction == 'short':
        return 'skip'
    
    return prediction