def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader trend is bearish (rsi_2h below 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts when broader trend is bullish (rsi_2h above 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction