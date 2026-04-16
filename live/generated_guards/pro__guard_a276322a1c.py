def guard(features: dict, prediction: str) -> str:
    """Skip trades when macd_histogram shows momentum deceleration."""
    macd = features.get("macd_histogram", 0)
    
    # Long entries: skip if momentum is decelerating (negative histogram)
    if prediction == "long" and macd < -0.0004:
        return "skip"
    
    # Short entries: skip if upside momentum is decelerating (positive histogram)
    if prediction == "short" and macd > 0.0004:
        return "skip"
    
    return prediction