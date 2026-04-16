def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and momentum indicators."""
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    macd_histogram = features.get("macd_histogram", 0.0)
    obv_slope = features.get("obv_slope", 0.0)
    stoch_k = features.get("stoch_k", 50.0)
    rsi_2h = features.get("rsi_2h", 50.0)
    
    # Detect compression: low ATR ratio AND narrow BB
    compression = atr_ratio < 0.8 and bb_width < 0.35
    
    # Count momentum indicators showing directional bias
    momentum_signals = 0
    if abs(macd_histogram) > 0.0005:
        momentum_signals += 1
    if obv_slope > 0 or obv_slope < 0:
        momentum_signals += 1
    if stoch_k < 25 or stoch_k > 75:
        momentum_signals += 1
    if rsi_2h < 35 or rsi_2h > 65:
        momentum_signals += 1
    
    # False compression: compression without momentum divergence
    if compression and momentum_signals < 2 and 0.3 < bb_pct_b < 0.7:
        return "skip"
    
    return prediction