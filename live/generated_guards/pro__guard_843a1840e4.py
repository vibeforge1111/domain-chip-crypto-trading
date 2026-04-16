def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration entries using MACD histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip long when momentum decelerating (negative histogram)
    if prediction == 'long' and macd_histogram < -0.0001:
        return "skip"
    
    # Skip short when momentum decelerating upward (positive histogram)
    if prediction == 'short' and macd_histogram > 0.0001:
        return "skip"
    
    # Additional filter: skip when stochastic confirms exhaustion against direction
    if prediction == 'long' and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    if prediction == 'short' and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction