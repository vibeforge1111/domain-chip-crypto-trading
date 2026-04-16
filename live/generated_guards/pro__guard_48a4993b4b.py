def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals - true consolidation needs healthy positioning."""
    bb_width = features.get("bb_width", 0.1)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Detect compression: both volatility indicators contracting
    is_compression = bb_width < 0.15 and atr_ratio < 0.8
    
    # False compression signals when price at extremes or momentum stretched
    false_compression = (bb_pct_b < 0.15 or bb_pct_b > 0.85 or 
                         stoch_k < 20 or stoch_k > 80 or
                         abs(vwap_dev) > 0.015)
    
    if is_compression and false_compression:
        return "skip"
    return prediction