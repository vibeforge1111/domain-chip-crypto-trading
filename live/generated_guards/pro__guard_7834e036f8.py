def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like rsi_2h, stoch_k, stoch_d, bb_pct_b, vwap_deviation, obv_slope, macd_histogram
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    return prediction