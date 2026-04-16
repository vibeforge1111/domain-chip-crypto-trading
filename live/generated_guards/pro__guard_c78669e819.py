def guard(features: dict, prediction: str) -> str:
    """Filter trades by aligning with broader 2h RSI trend context."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    if prediction == "long":
        if rsi_2h < 42:
            return "skip"
        if vwap_dev < -0.003:
            return "skip"
    
    if prediction == "short":
        if rsi_2h > 58:
            return "skip"
        if vwap_dev > 0.003:
            return "skip"
    
    return prediction