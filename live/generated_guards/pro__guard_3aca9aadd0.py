def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # In strong bullish broader trend (rsi_2h > 60), only allow longs
    if rsi_2h > 60 and prediction == "short":
        return "skip"
    
    # In strong bearish broader trend (rsi_2h < 40), only allow shorts
    if rsi_2h < 40 and prediction == "long":
        return "skip"
    
    return prediction