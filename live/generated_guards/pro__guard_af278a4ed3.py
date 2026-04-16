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
    
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV is declining (selling pressure)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip shorts when OBV is rising (buying pressure)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    # Additional filter: avoid trades against wider timeframe momentum
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction