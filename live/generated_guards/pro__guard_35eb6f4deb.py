def guard(features: dict, prediction: str) -> str:
    """Detect overbought/oversold extremes using BB position and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought extreme: both BB near upper band AND Stochastic overbought
    overbought_extreme = bb_pct_b > 0.90 and stoch_k > 85
    # Oversold extreme: both BB near lower band AND Stochastic oversold
    oversold_extreme = bb_pct_b < 0.10 and stoch_k < 15
    
    # Reject longs in overbought extremes, shorts in oversold extremes
    if prediction == 'long' and overbought_extreme:
        return 'skip'
    if prediction == 'short' and oversold_extreme:
        return 'skip'
    
    return prediction