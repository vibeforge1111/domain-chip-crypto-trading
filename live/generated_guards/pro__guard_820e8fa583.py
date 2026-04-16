def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum shows deceleration via MACD histogram."""
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs if MACD histogram negative (momentum decelerating) and 2h RSI not oversold
    if prediction == "long" and macd_hist < 0 and rsi_2h > 40:
        return "skip"
    
    # Skip shorts if MACD histogram positive (momentum accelerating) and 2h RSI not overbought
    if prediction == "short" and macd_hist > 0 and rsi_2h < 60:
        return "skip"
    
    return prediction