def guard(features: dict, prediction: str) -> str:
    """Filter trades misaligned with broader 2h trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Align long entries with bullish 2h context, avoid overbought
    if prediction == "long" and rsi_2h > 68:
        return "skip"
    
    # Align short entries with bearish 2h context, avoid oversold
    if prediction == "short" and rsi_2h < 32:
        return "skip"
    
    return prediction