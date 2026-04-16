def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR + BB width combination."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_position = features.get("bb_pct_b", 0.5)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect compression: low ATR + tight BB
    is_compression = atr_ratio < 0.7 and bb_width < 0.15
    
    # True compression: price near middle of BB, not at extremes
    is_mid_range = 0.25 < bb_position < 0.75
    
    # False compression: compression but price at extreme or 2h RSI extreme
    is_false_compression = is_compression and (not is_mid_range or rsi_2h < 30 or rsi_2h > 70)
    
    if is_false_compression:
        return "skip"
    
    return prediction