def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using RSI_2H and momentum."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Longs need bullish 2h context and positive momentum
    if prediction == "long" and (rsi_2h < 45 or macd_histogram < 0):
        return "skip"
    # Shorts need bearish 2h context and negative momentum
    if prediction == "short" and (rsi_2h > 55 or macd_histogram > 0):
        return "skip"
    
    return prediction