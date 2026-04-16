def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Momentum deceleration check: histogram near zero indicates weakening momentum
    if abs(macd_hist) < 0.0001:
        return "skip"
    
    # Validate momentum aligns with prediction direction and strength
    if prediction == "long":
        if macd_hist <= 0 or stoch_k > 85:
            return "skip"
    elif prediction == "short":
        if macd_hist >= 0 or stoch_k < 15:
            return "skip"
    
    return prediction