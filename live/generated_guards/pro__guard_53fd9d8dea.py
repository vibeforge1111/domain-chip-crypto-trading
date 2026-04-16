def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2-hour RSI and momentum confirmation."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Align with broader 2h trend
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    # Require momentum confirmation
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    return prediction