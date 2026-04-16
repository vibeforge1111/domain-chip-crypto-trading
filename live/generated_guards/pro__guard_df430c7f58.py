def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration via macd_histogram."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    
    # Reject longs when momentum is bearish (negative histogram = deceleration)
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    
    # Reject shorts when momentum is bullish (positive histogram = deceleration)
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    return prediction