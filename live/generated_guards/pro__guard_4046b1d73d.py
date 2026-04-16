def guard(features: dict, prediction: str) -> str:
    """Quality signal filter combining candle structure, volume, and volatility."""
    if prediction == "skip":
        return prediction
    
    # Reject doji-like candles (weak conviction)
    if features["body_ratio"] < 0.15:
        return "skip"
    
    # Reject low volume signals (potential noise)
    if features["volume_ratio"] < 0.6:
        return "skip"
    
    # Reject extreme volatility environments
    if features["atr_ratio"] > 2.5 or features["atr_ratio"] < 0.4:
        return "skip"
    
    return prediction