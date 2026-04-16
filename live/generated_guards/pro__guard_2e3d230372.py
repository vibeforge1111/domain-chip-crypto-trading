def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration against direction."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    
    # For long entries: reject if momentum is bearish (histogram negative)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # For short entries: reject if momentum is bullish (histogram positive)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction