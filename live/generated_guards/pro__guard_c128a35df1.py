def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram signals momentum deceleration."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Long: reject if MACD histogram is negative (no bullish momentum)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Long: reject if stochastics overbought (momentum exhausted)
    if prediction == "long" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    # Short: reject if MACD histogram is positive (no bearish momentum)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    # Short: reject if stochastics oversold (momentum exhausted for bears)
    if prediction == "short" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction