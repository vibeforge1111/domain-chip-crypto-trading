def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compressions using ATR/Bollinger combo."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.1)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = abs(features.get("vwap_deviation", 0))
    
    # True compression: low volatility + tight bands
    is_compressed = atr_ratio < 0.7 and bb_width < 0.8
    
    if is_compressed:
        # False compression: price at extremes or far from VWAP
        at_extreme = bb_pct_b < 0.2 or bb_pct_b > 0.8
        far_from_vwap = vwap_dev > 0.005
        
        if at_extreme or far_from_vwap:
            return "skip"
    
    return prediction