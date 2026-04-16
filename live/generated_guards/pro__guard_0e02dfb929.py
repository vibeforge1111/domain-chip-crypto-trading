def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2h trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long when 2h RSI deeply overbought (potential reversal risk)
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    # Skip short when 2h RSI deeply oversold (potential reversal risk)
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction