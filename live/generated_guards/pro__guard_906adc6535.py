def guard(features: dict, prediction: str) -> str:
    """Filter trades by aligning with broader 2-hour RSI trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h")
    if rsi_2h is None:
        return prediction
    
    # Long entries only when broader trend is bullish (rsi_2h > 55)
    if prediction == "long" and rsi_2h < 55:
        return "skip"
    
    # Short entries only when broader trend is bearish (rsi_2h < 45)
    if prediction == "short" and rsi_2h > 45:
        return "skip"
    
    return prediction