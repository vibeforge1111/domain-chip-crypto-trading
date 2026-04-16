def guard(features: dict, prediction: str) -> str:
    """Filter trades using BB position + momentum divergence and candle conviction."""
    bb_pos = features.get('bb_position', 0.5)
    momentum = features.get('momentum_score', 0)
    body_ratio = features.get('body_ratio', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # Skip if momentum contradicts BB position (potential reversal)
    if bb_pos > 0.85 and momentum < -0.2:
        return "skip"
    if bb_pos < 0.15 and momentum > 0.2:
        return "skip"
    
    # Skip if doji-like candle without strong volatility to justify it
    if body_ratio < 0.1 and atr_ratio < 1.2:
        return "skip"
    
    return prediction