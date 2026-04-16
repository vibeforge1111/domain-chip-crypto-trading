def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Detect momentum deceleration via shrinking/negative MACD histogram
    if prediction == "long":
        # Skip if MACD histogram is negative (bullish momentum weakening)
        if macd_histogram < -0.0002:
            return "skip"
        # Skip if stochastics overbought and RSI_2h extended
        if stoch_k > 80 and stoch_d > 70 and rsi_2h > 65:
            return "skip"
        # Skip if price too extended above VWAP
        if vwap_deviation > 0.015:
            return "skip"
    
    if prediction == "short":
        # Skip if MACD histogram is positive (bearish momentum weakening)
        if macd_histogram > 0.0002:
            return "skip"
        # Skip if stochastics oversold and RSI_2h low
        if stoch_k < 20 and stoch_d < 30 and rsi_2h < 35:
            return "skip"
        # Skip if price too extended below VWAP
        if vwap_deviation < -0.015:
            return "skip"
    
    return prediction