def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR and Bollinger Band width."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.5)
    
    # True compression: both metrics are low (calm, tight bands)
    # False compression: tight bands but high actual volatility
    is_tight_bands = bb_width < 0.5
    is_high_atr = atr_ratio > 0.75
    
    # Skip false compression: tight BB bands with elevated ATR (hidden volatility)
    if is_tight_bands and is_high_atr:
        return "skip"
    
    return prediction