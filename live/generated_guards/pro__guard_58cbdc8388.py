def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating against direction."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Momentum deceleration: longs need positive macd, shorts need negative
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Additional filter: avoid counter-trend longs at overbought, shorts at oversold
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction