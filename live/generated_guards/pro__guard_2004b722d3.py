def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs, require bullish broader trend
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # For shorts, require bearish broader trend
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction