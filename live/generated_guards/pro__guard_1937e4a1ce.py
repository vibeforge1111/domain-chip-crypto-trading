def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression to detect true vs false breakouts."""
    bb_width = features.get("bb_width", 0.1)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_histogram = features.get("macd_histogram", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: both bb_width and atr_ratio are low
    is_compressed = bb_width < 0.15 and atr_ratio < 0.7
    
    # Check for false compression: stoch divergence
    stoch_divergent = abs(stoch_k - stoch_d) > 25
    
    # Reject compressed but divergent signals (false compression)
    if is_compressed and stoch_divergent:
        return "skip"
    
    # Reject if far from VWAP during compression (weak positioning)
    if is_compressed and abs(vwap_deviation) > 0.02:
        return "skip"
    
    return prediction