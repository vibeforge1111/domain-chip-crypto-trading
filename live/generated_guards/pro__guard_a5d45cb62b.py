def guard(features: dict, prediction: str) -> str:
    """Filter trades on momentum deceleration using MACD histogram."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when MACD histogram negative (momentum decelerating) + overbought stoch
    if prediction == "long" and macd_hist < -0.0005 and stoch_k > 80:
        return "skip"
    
    # Reject shorts when MACD histogram positive (momentum decelerating up) + oversold stoch
    if prediction == "short" and macd_hist > 0.0005 and stoch_k < 20:
        return "skip"
    
    # Skip if extreme 2h RSI divergence from direction
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction