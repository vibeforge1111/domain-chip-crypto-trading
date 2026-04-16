def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    # Momentum deceleration: macd_histogram opposite to direction and stoch confirming exhaustion
    if prediction == 'long' and macd_histogram < 0 and stoch_k > 75:
        return 'skip'
    if prediction == 'short' and macd_histogram > 0 and stoch_k < 25:
        return 'skip'
    
    # Additional filter: reject if macd histogram strongly opposes trade direction
    if prediction == 'long' and macd_histogram < -0.0003:
        return 'skip'
    if prediction == 'short' and macd_histogram > 0.0003:
        return 'skip'
    
    return prediction