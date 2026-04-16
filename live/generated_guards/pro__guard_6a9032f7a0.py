def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration using MACD histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject longs when MACD histogram shows bearish momentum
    if prediction == "long" and macd_histogram < -0.0003:
        return "skip"
    
    # Reject shorts when MACD histogram shows bullish momentum
    if prediction == "short" and macd_histogram > 0.0003:
        return "skip"
    
    # Avoid entries at stochastic extremes
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    # Higher timeframe RSI alignment filter
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction