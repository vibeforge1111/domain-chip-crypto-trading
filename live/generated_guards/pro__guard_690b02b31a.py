def guard(features: dict, prediction: str) -> str:
    """Filter trades that conflict with broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Longs need bullish 2h context, shorts need bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction