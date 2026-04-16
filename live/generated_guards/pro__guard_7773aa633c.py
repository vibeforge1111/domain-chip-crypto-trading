def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when 2h RSI is bearish (<50)
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    # Skip shorts when 2h RSI is bullish (>50)
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction