def guard(features: dict, prediction: str) -> str:
    """Detect false compression - low BB width but high ATR ratio signals breakout risk."""
    bb_width = features.get("bb_width", 0)
    atr_ratio = features.get("atr_ratio", 1)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # False compression: tight bands but volatility expanding (about to explode)
    false_compression = bb_width < 0.025 and atr_ratio > 1.4
    
    # Also skip if near band edge during compression (likely mean reversion trap)
    near_extreme = bb_pct_b < 0.08 or bb_pct_b > 0.92
    
    if false_compression or near_extreme:
        return "skip"
    
    return prediction