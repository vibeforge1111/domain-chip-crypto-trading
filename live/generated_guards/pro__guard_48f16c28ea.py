def guard(features: dict, prediction: str) -> str:
    """Rejects trades when momentum/RSI contradict the signal direction."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    bb_position = features.get("bb_position", 0.5)
    atr_ratio = features.get("atr_ratio", 1.0)
    
    # For longs: reject if overbought, negative momentum, or near upper band
    if prediction == "long":
        if rsi > 70 or momentum < -0.2 or bb_position > 0.85 or atr_ratio > 2.0:
            return "skip"
    
    # For shorts: reject if oversold, positive momentum, or near lower band
    if prediction == "short":
        if rsi < 30 or momentum > 0.2 or bb_position < 0.15 or atr_ratio > 2.0:
            return "skip"
    
    return prediction