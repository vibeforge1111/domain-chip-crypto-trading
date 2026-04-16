def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long signals only valid when broader trend is bullish (rsi_2h >= 50)
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # Short signals only valid when broader trend is bearish (rsi_2h <= 50)
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction