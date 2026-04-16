def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB position and Stochastic show extreme conditions."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: price at upper band AND stoch confirming overbought
    overbought = bb_pct_b > 0.85 and stoch_k > 75
    
    # Oversold: price at lower band AND stoch confirming oversold
    oversold = bb_pct_b < 0.15 and stoch_k < 25
    
    # Skip longs in overbought, skip shorts in oversold
    if prediction == 'long' and overbought:
        return 'skip'
    if prediction == 'short' and oversold:
        return 'skip'
    
    return prediction