def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression breakouts - reject false breakouts at BB extremes."""
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: both bb_width and atr_ratio are low
    is_compression = bb_width < 0.7 and atr_ratio < 0.8
    
    if is_compression and prediction != "skip":
        # False breakout risk: price at BB extremes during compression
        at_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
        stoch_extreme = stoch_k < 20 or stoch_k > 80
        
        if at_extreme or stoch_extreme:
            return "skip"
    
    return prediction