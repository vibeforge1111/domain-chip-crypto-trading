def guard(features: dict, prediction: str) -> str:
    """Filter trades misaligned with broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader timeframe is bearish (rsi_2h < 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts when broader timeframe is bullish (rsi_2h > 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction