def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2h RSI and stochastics."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject longs when broader trend is weak (low 2h RSI)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Reject shorts when broader trend is strong (high 2h RSI)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Reject if short-term momentum contradicts trade direction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction