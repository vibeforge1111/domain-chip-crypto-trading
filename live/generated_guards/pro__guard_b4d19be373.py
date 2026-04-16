def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating (macd_histogram near zero)."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject if momentum is in transition zone (abs near zero = deceleration)
    if abs(macd_histogram) < 0.00015:
        return "skip"
    
    # Additional filter: weak momentum with low stochastic confirms deceleration
    if prediction == "long" and macd_histogram < 0.0003 and stoch_k < 65:
        return "skip"
    
    if prediction == "short" and macd_histogram > -0.0003 and stoch_k > 35:
        return "skip"
    
    return prediction