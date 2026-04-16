def guard(features: dict, prediction: str) -> str:
    """Filter trades on momentum deceleration using macd_histogram."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip longs if macd_histogram is negative (bearish momentum)
    if prediction == 'long' and macd_hist < -0.0002:
        return 'skip'
    
    # Skip shorts if macd_histogram is positive (bullish momentum)
    if prediction == 'short' and macd_hist > 0.0002:
        return 'skip'
    
    # Additional check: skip if stochastic shows extreme reading misaligned with prediction
    if prediction == 'long' and stoch_k > 80 and stoch_d > 80:
        return 'skip'
    if prediction == 'short' and stoch_k < 20 and stoch_d < 20:
        return 'skip'
    
    return prediction