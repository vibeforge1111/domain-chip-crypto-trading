def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak or decelerating momentum using MACD histogram."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if momentum is flat/neutral (macd_hist near zero)
    if abs(macd_hist) < 0.0001:
        return "skip"
    
    # Long entries require positive macd_histogram (bullish momentum)
    if prediction == "long" and macd_hist <= 0:
        return "skip"
    
    # Short entries require negative macd_histogram (bearish momentum)
    if prediction == "short" and macd_hist >= 0:
        return "skip"
    
    # Additional filter: avoid longs when overbought (reversal risk)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    
    # Avoid shorts when oversold (reversal risk)
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction