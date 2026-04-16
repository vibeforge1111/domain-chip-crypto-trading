def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2h RSI."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader trend is bearish
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    
    # Skip shorts when broader trend is bullish
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    return prediction