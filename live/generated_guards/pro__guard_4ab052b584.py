def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compression signals."""
    bb_width = features.get("bb_width", 0.02)
    atr_ratio = features.get("atr_ratio", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_histogram = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Detect compression: both bb_width and atr_ratio are low
    is_compressed = bb_width < 0.015 and atr_ratio < 0.7
    
    # Check for weak momentum during compression
    momentum_weak = abs(stoch_k - 50) < 15 and abs(stoch_d - 50) < 15
    momentum_weak = momentum_weak and abs(macd_histogram) < 0.0002
    momentum_weak = momentum_weak and abs(obv_slope) < 0.1
    
    # Skip if compressed but momentum is weak (false compression)
    if is_compressed and momentum_weak:
        return "skip"
    
    return prediction