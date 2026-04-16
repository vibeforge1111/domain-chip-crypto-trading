def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Detects momentum deceleration using MACD histogram before entry.
    """
    macd_histogram = features.get('macd_histogram', 0)
    
    # Reject long signals when momentum is decelerating (negative histogram)
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    
    # Reject short signals when momentum is accelerating (positive histogram)
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    return prediction