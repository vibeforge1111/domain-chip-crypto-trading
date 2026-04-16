def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD momentum is decelerating toward zero."""
    if prediction == "skip":
        return "skip"
    
    macd = features.get("macd_histogram", 0)
    
    # Reject longs when MACD histogram is weak/approaching zero (momentum decelerating)
    if prediction == "long" and 0 < macd < 0.00025:
        return "skip"
    
    # Reject shorts when MACD histogram is weak/approaching zero (momentum decelerating)
    if prediction == "short" and -0.00025 < macd < 0:
        return "skip"
    
    return prediction