def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups: true compression needs low volatility + middle-band position."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.5)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # True compression: low atr_ratio + narrow bands
    is_low_vol_compression = atr_ratio < 0.7 and bb_width < 0.3
    
    # False compression: price at extreme + momentum misaligned
    is_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
    momentum_weak = stoch_k < 30 or stoch_d < 30
    
    # Skip if compression is likely false (extreme position + weak momentum)
    if is_low_vol_compression and is_extreme and momentum_weak:
        return "skip"
    
    return prediction