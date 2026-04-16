def guard(features: dict, prediction: str) -> str:
    """Reject weak signals during volatility expansion with small bodies."""
    small_body = features.get('body_ratio', 1) < 0.25
    low_volume = features.get('volume_ratio', 1) < 0.85
    high_atr = features.get('atr_ratio', 1) > 1.15
    
    if small_body and low_volume and high_atr:
        return "skip"
    
    return prediction