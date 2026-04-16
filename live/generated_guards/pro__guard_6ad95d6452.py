def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Skip if too close to VWAP (no directional edge from fair value)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip if stochastic overbought with bearish MACD divergence
    if features.get('stoch_k', 50) > 80 and features.get('macd_histogram', 0) < -0.0001:
        return "skip"
    # Skip if 2h RSI confirms exhaustion against the trade direction
    if features.get('rsi_2h', 50) > 70 and prediction == "long":
        return "skip"
    if features.get('rsi_2h', 50) < 30 and prediction == "short":
        return "skip"
    return prediction