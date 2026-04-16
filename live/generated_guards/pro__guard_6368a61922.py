def guard(features: dict, prediction: str) -> str:
    """Reject trades where momentum is decelerating against the signal direction."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    
    # For long signals: reject if momentum is bearish (negative histogram)
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    
    # For short signals: reject if momentum is bullish (positive histogram)
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    return prediction