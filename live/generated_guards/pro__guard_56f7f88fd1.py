def guard(features: dict, prediction: str) -> str:
    """Filter trades against broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Align with broader trend: skip longs in bearish 2h context, skip shorts in bullish
    if prediction == "long" and rsi_2h > 65:
        return "skip"
    if prediction == "short" and rsi_2h < 35:
        return "skip"
    
    return prediction