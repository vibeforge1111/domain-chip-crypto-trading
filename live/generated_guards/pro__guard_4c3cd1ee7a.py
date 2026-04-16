def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram indicates momentum deceleration."""
    macd_histogram = features.get("macd_histogram", 0)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long entries: skip if momentum is fading (negative histogram) or RSI stretched
    if prediction == "long" and (macd_histogram < -0.0002 or rsi_14 > 72):
        return "skip"
    
    # Short entries: skip if upside momentum decelerating or RSI oversold
    if prediction == "short" and (macd_histogram > 0.0002 or rsi_14 < 28):
        return "skip"
    
    return prediction