def guard(features: dict, prediction: str) -> str:
    """Filter trades conflicting with broader 2h trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long entries need bullish 2h context (rsi_2h > 50)
    if prediction == "long" and rsi_2h < 48:
        return "skip"
    
    # Short entries need bearish 2h context (rsi_2h < 50)
    if prediction == "short" and rsi_2h > 52:
        return "skip"
    
    return prediction