def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR, Bollinger width, and momentum."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_histogram = features.get("macd_histogram", 0.0)
    obv_slope = features.get("obv_slope", 0.0)
    
    # Detect compression: both low ATR and narrow BB
    is_compressed = atr_ratio < 0.7 and bb_width < 0.02
    
    if is_compressed:
        # Momentum divergence check: stoch extremes or flat macd
        weak_momentum = (stoch_k < 20 or stoch_k > 80) and abs(macd_histogram) < 0.0005
        # Weak volume confirmation
        weak_volume = obv_slope < 0 and prediction == "long"
        weak_volume_rev = obv_slope > 0 and prediction == "short"
        
        if weak_momentum or weak_volume or weak_volume_rev:
            return "skip"
    
    return prediction