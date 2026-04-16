def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Only allow trades at extreme Bollinger Band positions with confirmation
    if bb_pct_b < 0.05:
        # Lower band extreme - only allow longs if stoch confirms oversold
        if stoch_k < 20 and vwap_deviation < 0:
            return prediction
        return "skip"
    elif bb_pct_b > 0.95:
        # Upper band extreme - only allow shorts if stoch confirms overbought
        if stoch_k > 80 and vwap_deviation > 0:
            return prediction
        return "skip"
    
    return "skip"