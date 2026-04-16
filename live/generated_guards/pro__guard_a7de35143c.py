def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    # Skip longs at extreme overbought: BB at upper band + stochastic overbought
    if prediction == 'long' and bb_pct_b > 0.90 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts at extreme oversold: BB at lower band + stochastic oversold
    if prediction == 'short' and bb_pct_b < 0.10 and stoch_k < 20:
        return 'skip'
    
    return prediction