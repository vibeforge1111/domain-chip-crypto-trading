def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI extremes and opposing wick dominance."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    
    # Reject long signals when overbought AND upper wick dominates (selling pressure)
    if prediction == "long" and rsi > 65 and upper_wick > 0.35:
        return "skip"
    
    # Reject short signals when oversold AND lower wick dominates (buying pressure)
    if prediction == "short" and rsi < 35 and lower_wick > 0.35:
        return "skip"
    
    return prediction