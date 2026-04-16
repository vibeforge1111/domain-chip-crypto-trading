def guard(features: dict, prediction: str) -> str:
    """Filter signals during false compression vs true breakouts."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    obv_slope = features.get("obv_slope", 0.0)
    rsi_2h = features.get("rsi_2h", 50.0)
    macd_histogram = features.get("macd_histogram", 0.0)
    
    # Detect compression: both ATR and BB contracting
    is_compressed = atr_ratio < 0.7 and bb_width < 0.15
    
    if is_compressed:
        # False compression: compressed but no momentum or accumulation
        weak_momentum = abs(obv_slope) < 0.001 and abs(macd_histogram) < 0.0001
        neutral_2h = 40 < rsi_2h < 60
        mid_band = 0.35 < bb_pct_b < 0.65
        
        if weak_momentum and neutral_2h and mid_band:
            return "skip"
    
    return prediction