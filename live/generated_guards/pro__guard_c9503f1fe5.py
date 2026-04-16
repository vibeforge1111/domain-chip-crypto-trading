def guard(features: dict, prediction: str) -> str:
    """Filter trades against broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader timeframe is bearish (divergence risk)
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    
    # Skip shorts when broader timeframe is bullish (divergence risk)
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    return prediction