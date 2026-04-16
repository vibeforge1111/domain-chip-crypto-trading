def guard(features: dict, prediction: str) -> str:
    """Reject trades during volatility compression squeeze with extended price."""
    bb_width = features.get('bb_width', 1.0)
    volatility_regime = features.get('volatility_regime', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_position = features.get('bb_position', 0.5)
    
    # Volatility compression detected
    is_squeeze = bb_width < 0.5 or (volatility_regime < 0.3 and atr_ratio < 0.8)
    
    # Price extended from center (near extremes)
    is_extended = bb_position > 0.85 or bb_position < 0.15
    
    # Reject breakout attempts during squeeze
    if is_squeeze and is_extended:
        return "skip"
    
    return prediction