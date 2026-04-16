def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating using MACD histogram."""
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect momentum deceleration: long entry when histogram turning negative
    if prediction == "long" and macd_histogram < -0.0002:
        return "skip"
    
    # Detect momentum deceleration: short entry when histogram turning positive
    if prediction == "short" and macd_histogram > 0.0002:
        return "skip"
    
    # Additional filter: reject longs with weakening momentum + overbought 2h RSI
    if prediction == "long" and macd_histogram < 0 and rsi_2h > 70:
        return "skip"
    
    # Additional filter: reject shorts with weakening momentum + oversold 2h RSI
    if prediction == "short" and macd_histogram > 0 and rsi_2h < 30:
        return "skip"
    
    return prediction