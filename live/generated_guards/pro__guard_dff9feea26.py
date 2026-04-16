def guard(features: dict, prediction: str) -> str:
    """Reject trades when candle wick contradicts direction + momentum is weak."""
    if prediction == "skip":
        return prediction
    
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    
    # Long signals: reject if large upper wick (selling pressure) with overbought RSI
    if prediction == "long":
        if upper_wick > 0.4 and rsi > 65 and momentum < 0:
            return "skip"
    
    # Short signals: reject if large lower wick (buying pressure) with oversold RSI
    if prediction == "short":
        if lower_wick > 0.4 and rsi < 35 and momentum > 0:
            return "skip"
    
    return prediction