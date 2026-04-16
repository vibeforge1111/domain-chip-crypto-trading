def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI extremes and trend strength."""
    rsi = features.get("rsi_14", 50)
    trend = features.get("trend_strength", 0.5)
    momentum = features.get("momentum_score", 0.5)
    
    # Skip long signals when RSI overbought AND weak trend
    if prediction == "long" and rsi > 70 and trend < 0.4:
        return "skip"
    
    # Skip short signals when RSI oversold AND weak trend
    if prediction == "short" and rsi < 30 and trend < 0.4:
        return "skip"
    
    # Skip trades with low momentum
    if momentum < 0.3:
        return "skip"
    
    return prediction