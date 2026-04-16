def guard(features: dict, prediction: str) -> str:
    """Filter trades at Bollinger Band and Stochastic overbought/oversold extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject longs at overbought extremes (top of bands + overbought stochastic)
    if prediction == 'long' and bb_pct_b > 0.92 and stoch_k > 80:
        return 'skip'
    
    # Reject shorts at oversold extremes (bottom of bands + oversold stochastic)
    if prediction == 'short' and bb_pct_b < 0.08 and stoch_k < 20:
        return 'skip'
    
    return prediction