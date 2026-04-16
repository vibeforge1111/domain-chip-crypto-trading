def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI trend alignment."""
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Skip if 2h RSI is overbought (reversal risk) or very weak
        if rsi_2h > 72 or rsi_2h < 38:
            return "skip"
    elif prediction == "short":
        # Skip if 2h RSI is oversold (reversal risk) or still strong
        if rsi_2h < 28 or rsi_2h > 62:
            return "skip"
    
    return prediction