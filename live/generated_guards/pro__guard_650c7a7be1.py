def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader trend is bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts when broader trend is bullish
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction