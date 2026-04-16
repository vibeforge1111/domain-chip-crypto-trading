def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating against the direction."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    
    # Momentum deceleration: reject if histogram opposes prediction direction
    if prediction == "long" and macd < -0.0001:
        return "skip"
    
    if prediction == "short" and macd > 0.0001:
        return "skip"
    
    return prediction