def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is diverging from direction."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long' and macd < -0.0001:
        return 'skip'
    if prediction == 'short' and macd > 0.0001:
        return 'skip'
    if prediction == 'long' and stoch_k < stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k > stoch_d:
        return 'skip'
    
    return prediction