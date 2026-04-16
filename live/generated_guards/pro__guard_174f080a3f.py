def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when broader RSI is oversold (trend too weak)
    if prediction == "long" and rsi_2h < 42:
        return "skip"
    
    # Reject shorts when broader RSI is overbought (trend too strong)
    if prediction == "short" and rsi_2h > 58:
        return "skip"
    
    return prediction