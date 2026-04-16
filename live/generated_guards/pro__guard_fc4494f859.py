def guard(features: dict, prediction: str) -> str:
    """Filter trades at Bollinger Band and Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Overbought: BB near upper band + elevated stochastic
    overbought = bb_pct_b > 0.85 and stoch_k > 80 and stoch_d > 75
    # Oversold: BB near lower band + depressed stochastic
    oversold = bb_pct_b < 0.15 and stoch_k < 20 and stoch_d < 25
    
    # Skip longs at overbought extremes, shorts at oversold extremes
    if prediction == 'long' and overbought:
        return 'skip'
    if prediction == 'short' and oversold:
        return 'skip'
    
    return prediction