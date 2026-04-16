def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    
    # Momentum deceleration: histogram near zero (flat) or opposing direction
    if prediction == "long" and macd < 0.0001:
        return "skip"
    if prediction == "short" and macd > -0.0001:
        return "skip"
    
    return prediction