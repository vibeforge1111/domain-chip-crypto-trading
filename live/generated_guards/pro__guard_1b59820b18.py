def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend using rsi_2h."""
    if prediction == "skip":
        return "skip"
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long trades need bullish 2h context
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Short trades need bearish 2h context
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction