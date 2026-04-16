def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Reject long if MACD histogram is negative (momentum weakening)
    if prediction == "long" and macd_histogram < -0.0002:
        return "skip"
    
    # Reject short if MACD histogram is positive (momentum strengthening)
    if prediction == "short" and macd_histogram > 0.0002:
        return "skip"
    
    # Additional confirmation: reject longs when volume diverging from price (negative OBV slope)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    return prediction