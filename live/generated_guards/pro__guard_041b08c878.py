def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and confirming indicators."""
    if prediction == "skip":
        return prediction
    
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # True compression: low bb_width + low atr_ratio
    is_compression = bb_width < 0.15 and atr_ratio < 0.7
    
    if is_compression:
        # False compression signals: extreme stoch, VWAP far away, momentum diverging
        stoch_extreme = stoch_k > 80 or stoch_k < 20
        vwap_far = abs(vwap_deviation) > 0.02
        momentum_weak = abs(macd_histogram) < 0.0001
        
        # Check if position is too extreme within bands
        bb_extreme = bb_pct_b > 0.9 or bb_pct_b < 0.1
        
        # Reject if multiple false compression indicators present
        false_signals = sum([stoch_extreme, vwap_far, momentum_weak, bb_extreme])
        if false_signals >= 2:
            return "skip"
    
    return prediction