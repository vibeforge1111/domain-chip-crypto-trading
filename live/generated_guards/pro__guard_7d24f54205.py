def guard(features: dict, prediction: str) -> str:
    """Guard against false compression - only accept trades when compression is genuine."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression detected when both indicators show compression
    is_compressed = atr_ratio < 0.75 and bb_width < 0.18
    
    # False compression: compressed but price at extreme BB position
    extreme_position = bb_pct_b > 0.88 or bb_pct_b < 0.12
    
    # False compression: compressed but stoch overbought/oversold
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    
    # Weak accumulation/distribution during compression (potential fakeout)
    weak_momentum = is_compressed and abs(obv_slope) < 0.1
    
    if is_compressed and (extreme_position or stoch_extreme or weak_momentum):
        return "skip"
    
    return prediction