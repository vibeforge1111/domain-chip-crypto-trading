def guard(features: dict, prediction: str) -> str:
    """Filter trades by detecting true vs false compression using ATR and Bollinger Bands."""
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_2h = features.get("rsi_2h", 50)
    macd_histogram = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # True compression: both bb_width and atr_ratio are low
    is_compressed = (bb_width < 0.5) and (atr_ratio < 0.8)
    
    if not is_compressed:
        return prediction
    
    # In true compression, check momentum alignment
    is_bullish = (macd_histogram > 0) and (obv_slope > 0) and (rsi_2h > 45)
    is_bearish = (macd_histogram < 0) and (obv_slope < 0) and (rsi_2h < 55)
    
    # Extreme position within bands suggests breakout direction
    at_lower_extreme = bb_pct_b < 0.2
    at_upper_extreme = bb_pct_b > 0.8
    
    # In compression, only allow trades aligned with momentum and position
    if is_bullish or at_lower_extreme:
        if prediction == "long":
            return prediction
    if is_bearish or at_upper_extreme:
        if prediction == "short":
            return prediction
    
    return "skip"