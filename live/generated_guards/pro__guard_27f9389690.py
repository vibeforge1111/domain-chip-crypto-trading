def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum shows deceleration via MACD histogram."""
    macd_histogram = features.get("macd_histogram", 0)
    
    # Momentum should align with prediction direction
    # macd_histogram positive = bullish momentum, negative = bearish
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    return prediction