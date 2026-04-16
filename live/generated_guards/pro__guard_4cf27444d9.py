def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using BB width, ATR ratio, and divergence signals."""
    bb_width = features.get('bb_width', 0.2)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: both BB width and ATR compressed
    bb_compressed = bb_width < 0.15
    atr_compressed = atr_ratio < 0.8
    is_true_compression = bb_compressed and atr_compressed
    
    # False signal flags
    # 1. Price at extreme BB position (reversal risk)
    extreme_bb = bb_pct_b < 0.15 or bb_pct_b > 0.85
    # 2. Stochastic divergence
    stoch_divergence = abs(stoch_k - stoch_d) > 12
    # 3. No volume confirmation (OBV flat)
    no_volume = abs(obv_slope) < 0.001
    
    # Skip if true compression but multiple false signal indicators present
    if is_true_compression:
        if sum([extreme_bb, stoch_divergence, no_volume]) >= 2:
            return "skip"
    
    return prediction