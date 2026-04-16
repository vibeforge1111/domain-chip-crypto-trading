def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating based on MACD histogram."""
    macd = features.get("macd_histogram", 0)
    
    # Skip longs when MACD histogram is negative (bullish momentum weakening)
    if prediction == "long" and macd < 0:
        return "skip"
    
    # Skip shorts when MACD histogram is positive (bearish momentum weakening)
    if prediction == "short" and macd > 0:
        return "skip"
    
    return prediction