def guard(features: dict, prediction: str) -> str:
    """Guard against trades during momentum deceleration."""
    macd = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip longs if MACD histogram negative (bearish momentum)
    if prediction == "long" and macd < -0.0001:
        return "skip"
    
    # Skip shorts if MACD histogram positive (bullish momentum)
    if prediction == "short" and macd > 0.0001:
        return "skip"
    
    # Additional filter: avoid counter-trend entries near VWAP extremes
    if prediction == "long" and macd < 0 and vwap_dev > 0.01:
        return "skip"
    if prediction == "short" and macd > 0 and vwap_dev < -0.01:
        return "skip"
    
    return prediction