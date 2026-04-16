def guard(features: dict, prediction: str) -> str:
    """Reject entries when momentum decelerates against the direction."""
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long signals: skip if momentum is decelerating or higher timeframe overbought
    if prediction == "long" and (macd < -0.0005 or rsi_2h > 68):
        return "skip"
    # Short signals: skip if momentum is accelerating or higher timeframe oversold
    if prediction == "short" and (macd > 0.0005 or rsi_2h < 32):
        return "skip"
    return prediction