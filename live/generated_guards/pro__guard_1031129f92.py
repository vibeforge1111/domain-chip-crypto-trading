def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, stoch_k, stoch_d, rsi_2h, vwap_deviation
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long trades when OBV is declining (volume flow against longs)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip short trades when OBV is rising (volume flow against shorts)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    # Additional filter: skip longs if stoch overbought + 2h RSI weak
    if prediction == "long" and stoch_k > 80 and rsi_2h < 45:
        return "skip"
    
    return prediction