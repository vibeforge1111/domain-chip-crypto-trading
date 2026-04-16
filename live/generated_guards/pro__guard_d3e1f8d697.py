def guard(features: dict, prediction: str) -> str:
    """Reject mean reversion signals when momentum contradicts the signal direction."""
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    
    # Overbought but EMA flat/down - reject long signals
    if prediction == "long" and rsi > 70 and ema_slope <= 0.001:
        return "skip"
    
    # Oversold but EMA flat/up - reject short signals
    if prediction == "short" and rsi < 30 and ema_slope >= -0.001:
        return "skip"
    
    return prediction