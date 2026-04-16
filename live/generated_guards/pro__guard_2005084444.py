def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating using MACD histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Momentum deceleration zones near zero histogram
    near_zero = abs(macd_histogram) < 0.0003
    
    if prediction == 'long':
        # Reject if MACD momentum is decelerating toward zero
        if near_zero and macd_histogram > 0:
            return 'skip'
        # Reject longs at upper band with declining stoch momentum
        if bb_pct_b > 0.85 and stoch_k < stoch_d:
            return 'skip'
    
    if prediction == 'short':
        # Reject if bearish momentum is decelerating toward zero
        if near_zero and macd_histogram < 0:
            return 'skip'
        # Reject shorts at lower band with rising stoch momentum
        if bb_pct_b < 0.15 and stoch_k > stoch_d:
            return 'skip'
    
    return prediction