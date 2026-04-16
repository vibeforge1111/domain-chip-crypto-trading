def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and Bollinger Band width."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.02)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # True compression: both ATR and BB width are low
    is_compressed = atr_ratio < 0.85 and bb_width < 0.015
    
    if is_compressed:
        # False compression filter: price at extreme + volume spike = likely fakeout
        at_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
        volume_surge = volume_ratio > 2.0
        stoch_extreme = stoch_k < 15 or stoch_k > 85
        
        # Reject if multiple warning signs during compression
        warning_count = sum([at_extreme, volume_surge, stoch_extreme])
        if warning_count >= 2:
            return "skip"
    
    return prediction