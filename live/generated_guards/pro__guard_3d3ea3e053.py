def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, bb_pct_b, vwap_deviation, stoch_k, stoch_d, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long trades when OBV is declining (volume distribution)
    if prediction == "long" and obv_slope < -0.02:
        return "skip"
    
    # Skip short trades when OBV is rising (volume accumulation)
    if prediction == "short" and obv_slope > 0.02:
        return "skip"
    
    return prediction