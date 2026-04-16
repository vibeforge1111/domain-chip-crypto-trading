def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, macd_histogram, bb_pct_b, vwap_deviation, stoch_k, stoch_d, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs if OBV is declining (distribution) with MACD confirming weakness
    if prediction == "long" and obv_slope < -0.5 and macd_histogram < 0:
        return "skip"
    
    # Skip shorts if OBV is rising (accumulation) with 2h RSI showing strength
    if prediction == "short" and obv_slope > 0.5 and rsi_2h > 55:
        return "skip"
    
    return prediction