def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression to detect true vs false breakouts."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    vwap_dev = abs(features.get("vwap_deviation", 0))
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    macd_hist = features.get("macd_histogram", 0)
    
    # True compression: both atr and bb_width low, price near VWAP, not at extremes
    is_compression = atr_ratio < 0.75 and bb_width < 0.75
    
    if is_compression:
        # False compression: price drifted far from VWAP during compression
        if vwap_dev > 0.008:
            return "skip"
        # False compression: stochastic at extreme during compression (often reversal bait)
        if stoch_k < 20 or stoch_k > 80:
            if abs(macd_hist) > 0.0003:
                return "skip"
    
    return prediction