def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating against the direction."""
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration filter - macd_histogram sign opposes prediction
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    # Additional check: long when 2h RSI extremely overbought suggests reversal risk
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    return prediction