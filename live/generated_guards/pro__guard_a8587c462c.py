def guard(features: dict, prediction: str) -> str:
    """Filter trades when macd_histogram shows momentum deceleration."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration for longs: macd histogram negative
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    
    # Momentum deceleration for shorts: macd histogram positive
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    # Cross-timeframe divergence check - reject if 2h RSI contradicts direction
    if prediction == "long" and rsi_2h < 40 and rsi_14 > 60:
        return "skip"
    
    if prediction == "short" and rsi_2h > 60 and rsi_14 < 40:
        return "skip"
    
    return prediction