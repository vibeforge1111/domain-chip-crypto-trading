def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, bb_pct_b, vwap_deviation, stoch_k, stoch_d, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution), skip shorts when OBV is rising (accumulation)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction