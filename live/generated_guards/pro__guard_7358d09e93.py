def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2h RSI."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader trend is deeply oversold (may continue down)
    if prediction == "long" and rsi_2h < 30:
        return "skip"
    
    # Skip shorts when broader trend is deeply overbought (may continue up)
    if prediction == "short" and rsi_2h > 70:
        return "skip"
    
    return prediction