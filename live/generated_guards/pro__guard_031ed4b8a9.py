def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like macd_histogram, vwap_deviation, stoch_k, stoch_d, obv_slope, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Detect momentum deceleration: macd_histogram near zero (weakening momentum)
    # Combined with extended RSI on higher timeframe (potential reversal)
    if abs(macd_hist) < 0.0001 and rsi_2h > 70:
        return "skip"
    
    # Reject long entries when momentum fading AND price extended above VWAP
    if prediction == "long" and macd_hist < 0 and vwap_dev > 0.01:
        return "skip"
    
    # Reject short entries when momentum fading AND price deeply below VWAP
    if prediction == "short" and macd_hist < 0 and vwap_dev < -0.01:
        return "skip"
    
    return prediction