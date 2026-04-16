def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend context."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs, require broader 2h trend to be bullish
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # For shorts, require broader 2h trend to be bearish
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction