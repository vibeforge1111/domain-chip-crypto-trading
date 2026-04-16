def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals by detecting conflicting volatility indicators."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.0)
    
    # False compression: low volatility but wide bands = conflicting signals
    if atr_ratio < 0.7 and bb_width > 1.5:
        return "skip"
    
    return prediction