def guard(features: dict, prediction: str) -> str:
    """Guard against trading at Bollinger Band and Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject longs when both indicators show overbought extreme
    if prediction == 'long' and bb_pct_b > 0.92 and stoch_k > 85:
        return 'skip'
    
    # Reject shorts when both indicators show oversold extreme
    if prediction == 'short' and bb_pct_b < 0.08 and stoch_k < 15:
        return 'skip'
    
    return prediction