def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating based on MACD histogram."""
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect momentum deceleration: reject when MACD histogram contradicts direction
    # and wider timeframe RSI confirms exhaustion (deceleration signal)
    if prediction == "long" and macd_histogram < -0.0005 and rsi_2h > 65:
        return "skip"
    
    if prediction == "short" and macd_histogram > 0.0005 and rsi_2h < 35:
        return "skip"
    
    return prediction