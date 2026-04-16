def guard(features: dict, prediction: str) -> str:
    """Filter signals during false compression vs true compression."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # False compression: bands tight but volatility elevated
    if bb_width < 0.5 and atr_ratio > 0.7:
        return "skip"
    
    return prediction