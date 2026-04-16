def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum diverges from trade direction."""
    macd = features.get("macd_histogram", 0)
    
    # Skip long when macd_histogram is negative (bearish momentum)
    if prediction == "long" and macd < -0.0001:
        return "skip"
    
    # Skip short when macd_histogram is positive (bullish momentum)
    if prediction == "short" and macd > 0.0001:
        return "skip"
    
    return prediction