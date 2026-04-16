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
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration: reject longs with negative MACD, shorts with positive MACD
    if prediction == "long" and macd_hist < -0.0003:
        return "skip"
    
    if prediction == "short" and macd_hist > 0.0003:
        return "skip"
    
    # Combined exhaustion: overbought/oversold with conflicting momentum
    if prediction == "long" and stoch_k > 80 and macd_hist < 0:
        return "skip"
    
    if prediction == "short" and stoch_k < 20 and macd_hist > 0:
        return "skip"
    
    return prediction