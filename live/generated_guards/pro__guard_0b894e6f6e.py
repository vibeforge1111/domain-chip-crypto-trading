def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long entries need bullish 2h context (rsi_2h > 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    # Short entries need bearish 2h context (rsi_2h < 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction