def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR expansion + BB width."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: tight BB + rising ATR
    in_compression = bb_width < 0.2
    volatility_building = atr_ratio > 1.1
    
    # False signal: compression but no volatility expansion yet
    if in_compression and not volatility_building:
        return "skip"
    
    # Reject if prediction contradicts stoch momentum
    if prediction == "long" and stoch_k < 25:
        return "skip"
    if prediction == "short" and stoch_k > 75:
        return "skip"
    
    return prediction