def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = abs(features.get('vwap_deviation', 0))
    # Skip if too close to fair value (VWAP)
    if vwap_dev < 0.002:
        return "skip"
    # Skip long if overbought or short if oversold
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    return prediction