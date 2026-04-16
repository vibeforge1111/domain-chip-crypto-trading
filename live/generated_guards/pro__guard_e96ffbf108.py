def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if features['macd_histogram'] > 0.001 and features['stoch_k'] > 80:
        return "skip"
    
    if features['macd_histogram'] < -0.001 and features['stoch_k'] < 20:
        return "skip"
    
    if abs(features['macd_histogram']) < 0.0005 and abs(features['obv_slope']) < 0.1:
        return "skip"
    
    return prediction