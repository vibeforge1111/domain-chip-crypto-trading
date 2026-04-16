def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI to align with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long signals when broader timeframe is overbought
    if prediction == "long" and rsi_2h > 68:
        return "skip"
    
    # Skip short signals when broader timeframe is oversold
    if prediction == "short" and rsi_2h < 32:
        return "skip"
    
    return prediction