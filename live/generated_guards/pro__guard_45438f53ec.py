def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI to align with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2h RSI is overbought (>70) - broader trend may reverse
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    # Reject shorts when 2h RSI is oversold (<30) - broader trend may reverse
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction