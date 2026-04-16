def guard(features: dict, prediction: str) -> str:
    """Filter signals during compression phases using BB width and ATR ratio."""
    bb_width = features.get("bb_width", 0.02)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: tight BB + moderate ATR (not squeeze-fade)
    is_compression = bb_width < 0.015 and atr_ratio < 0.8
    
    # Reject if compression + price at BB extremes (false break setup)
    if is_compression and (bb_pct_b < 0.2 or bb_pct_b > 0.8):
        return "skip"
    
    # Reject if compression + extreme stochastic (exhaustion risk)
    if is_compression and (stoch_k < 15 or stoch_k > 85):
        return "skip"
    
    return prediction