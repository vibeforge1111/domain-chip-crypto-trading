def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating based on MACD histogram."""
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs: reject if MACD histogram is negative (momentum weakening)
    if prediction == "long" and macd < -0.0003:
        return "skip"
    
    # For shorts: reject if MACD histogram is positive (momentum weakening for shorts)
    if prediction == "short" and macd > 0.0003:
        return "skip"
    
    # Additional filter: reject longs when 2h RSI is overbought (>70)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Reject shorts when 2h RSI is oversold (<30)
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction