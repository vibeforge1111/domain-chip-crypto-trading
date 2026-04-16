def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow and wider timeframe conditions."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV declining (distribution) or 2h RSI overbought
    if prediction == "long":
        if obv_slope < -0.01:
            return "skip"
        if rsi_2h > 70:
            return "skip"
    
    # Skip shorts when OBV rising (accumulation) or 2h RSI oversold
    if prediction == "short":
        if obv_slope > 0.01:
            return "skip"
        if rsi_2h < 30:
            return "skip"
    
    return prediction