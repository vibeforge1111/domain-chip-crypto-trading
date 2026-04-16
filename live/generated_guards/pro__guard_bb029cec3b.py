def guard(features: dict, prediction: str) -> str:
    """Filters trades on volatility expansion without confirmation."""
    # Skip if ATR expands but volume/momentum don't confirm
    if features.get('atr_ratio', 0) > 1.5:
        if features.get('volume_ratio', 1) < 1.0 or features.get('momentum_score', 50) < 45:
            return "skip"
    
    # Skip if BB position is extreme without momentum support
    bb_pos = features.get('bb_position', 0.5)
    if bb_pos > 0.9 or bb_pos < 0.1:
        if features.get('momentum_score', 50) < 40:
            return "skip"
    
    return prediction