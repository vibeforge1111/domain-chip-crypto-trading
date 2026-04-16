def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long only when 2h RSI confirms bullish broader context
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    # Short only when 2h RSI confirms bearish broader context
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction