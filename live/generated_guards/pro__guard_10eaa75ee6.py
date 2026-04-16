def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio, BB width, and momentum."""
    # True compression requires BOTH low ATR ratio AND low BB width
    is_compressed = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 0) < 0.7
    if not is_compressed:
        return "skip"
    
    # Volume confirmation needed for true compression
    if features.get('volume_ratio', 0) < 0.8:
        return "skip"
    
    # Check momentum alignment with direction
    if prediction == "long":
        # Need bullish MACD, reasonable stoch (not overbought), VWAP not bearish
        if features.get('macd_histogram', 0) <= 0:
            return "skip"
        if features.get('stoch_k', 0) >= 80:
            return "skip"
        if features.get('vwap_deviation', 0) < -0.015:
            return "skip"
        if features.get('obv_slope', 0) <= 0:
            return "skip"
    elif prediction == "short":
        # Need bearish MACD, reasonable stoch (not oversold), VWAP not bullish
        if features.get('macd_histogram', 0) >= 0:
            return "skip"
        if features.get('stoch_k', 0) <= 20:
            return "skip"
        if features.get('vwap_deviation', 0) > 0.015:
            return "skip"
        if features.get('obv_slope', 0) >= 0:
            return "skip"
    
    return prediction