def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using BB width, ATR ratio, and broader context."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: narrow BB AND low ATR (volatility squeeze)
    is_compressed = bb_width < 0.4 and atr_ratio < 0.7
    if not is_compressed:
        return "skip"
    
    # Price should be near VWAP, not extended
    if abs(vwap_dev) > 0.012:
        return "skip"
    
    # Stochastic extremes signal reversal risk
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    # Align with broader trend
    if rsi_2h < 40 and prediction == "long":
        return "skip"
    if rsi_2h > 60 and prediction == "short":
        return "skip"
    
    return prediction