def guard(features: dict, prediction: str) -> str:
    """Filter trades by aligning with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader timeframe is bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts when broader timeframe is bullish
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction