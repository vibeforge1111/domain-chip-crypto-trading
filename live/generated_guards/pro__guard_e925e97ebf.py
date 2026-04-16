def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like macd_histogram, stoch_k, stoch_d, rsi_2h, vwap_deviation, bb_pct_b, obv_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Skip if not an active trade signal
    if prediction == "skip":
        return prediction

    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pos = features.get("bb_pct_b", 0.5)

    # Momentum deceleration filter using macd_histogram
    if prediction == "long":
        # Reject long if momentum is bearish (negative macd histogram)
        if macd < -0.0003:
            return "skip"
        # Reject if overbought on 2h and extended from VWAP
        if rsi_2h > 72 and vwap_dev < -0.002 and bb_pos > 0.85:
            return "skip"
    elif prediction == "short":
        # Reject short if momentum is bullish (positive macd histogram)
        if macd > 0.0003:
            return "skip"
        # Reject if oversold on 2h and extended from VWAP
        if rsi_2h < 28 and vwap_dev > 0.002 and bb_pos < 0.15:
            return "skip"

    return prediction