def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using ATR, BB width, and momentum indicators."""
    bb_width = features.get("bb_width", 0.02)
    atr_ratio = features.get("atr_ratio", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Detect compression: both BB width and ATR below thresholds
    is_compressed = bb_width < 0.015 and atr_ratio < 0.7
    
    if is_compressed:
        # False compression: stoch at extremes (exhausted momentum)
        stoch_exhausted = (stoch_k < 20 and stoch_d < 25) or (stoch_k > 80 and stoch_d > 75)
        
        # False compression: price too far from VWAP during compression
        vwap_unstable = abs(vwap_dev) > 0.015
        
        # False compression: compressed at band edge (not healthy consolidation)
        edge_compression = bb_pct_b < 0.15 or bb_pct_b > 0.85
        
        if stoch_exhausted or vwap_unstable or edge_compression:
            return "skip"
    
    return prediction