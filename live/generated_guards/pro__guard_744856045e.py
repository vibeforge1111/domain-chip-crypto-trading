def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI trend alignment."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Longs need bullish 2h context (rsi_2h above 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Shorts need bearish 2h context (rsi_2h below 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction