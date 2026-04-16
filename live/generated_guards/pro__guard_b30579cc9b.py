def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Reject longs if stochastic has already crossed too far (missed entry)
    if prediction == 'long' and stoch_k > stoch_d + 10:
        return 'skip'
    
    # Reject shorts if stochastic has already crossed too far down
    if prediction == 'short' and stoch_k < stoch_d - 10:
        return 'skip'
    
    # Verify momentum alignment with macd_histogram
    macd = features.get('macd_histogram', 0)
    if prediction == 'long' and macd < -0.0001:
        return 'skip'
    if prediction == 'short' and macd > 0.0001:
        return 'skip'
    
    return prediction