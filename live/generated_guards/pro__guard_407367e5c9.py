def guard(features: dict, prediction: str) -> str:
    """Reject signals with extreme RSI contradicting trend direction."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Strong RSI divergence from trend is unreliable
    rsi_extreme = rsi > 68 or rsi < 32
    if rsi_extreme:
        if prediction == "long" and ema_slope < 0:
            return "skip"
        if prediction == "short" and ema_slope > 0:
            return "skip"
    
    # Low body ratio indicates indecision candle
    if body_ratio < 0.25:
        return "skip"
    
    return prediction