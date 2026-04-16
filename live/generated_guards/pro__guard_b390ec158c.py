def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2h trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs in bearish broader trend (rsi_2h < 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts in bullish broader trend (rsi_2h > 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction