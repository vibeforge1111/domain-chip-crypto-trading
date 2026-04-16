def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0.2)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # True compression: low BB width AND low ATR ratio
    is_compressed = bb_width < 0.15 and atr_ratio < 0.7
    
    # At BB extremes: near 0 (lower) or near 1 (upper)
    at_extreme = bb_pct_b > 0.9 or bb_pct_b < 0.1
    
    # Momentum confirming reversal in 2h context
    momentum_confirm = (rsi_2h > 70 and stoch_k > 75) or (rsi_2h < 30 and stoch_k < 25)
    
    if is_compressed and at_extreme and momentum_confirm:
        return "skip"
    
    return prediction