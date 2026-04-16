def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram contradicts direction (momentum deceleration)."""
    macd = features.get("macd_histogram", 0)
    
    # Long trades need positive macd momentum
    if prediction == "long" and macd < -0.0002:
        return "skip"
    
    # Short trades need negative macd momentum
    if prediction == "short" and macd > 0.0002:
        return "skip"
    
    return prediction