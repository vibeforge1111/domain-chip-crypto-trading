def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs, require bullish broader trend (rsi_2h >= 50)
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # For shorts, require bearish broader trend (rsi_2h < 50)
    if prediction == "short" and rsi_2h >= 50:
        return "skip"
    
    return prediction