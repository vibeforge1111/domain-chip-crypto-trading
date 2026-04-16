def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and Bollinger width."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # True compression: low volatility + tight bands
    is_compressed = atr_ratio < 0.7 and bb_width < 0.25
    
    # False compression risk: stoch extremes during compression suggest trap setups
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    stoch_divergence = abs(stoch_k - stoch_d) > 15
    
    # Skip if compressed with exhausted momentum or hidden divergence
    if is_compressed and stoch_extreme and stoch_divergence:
        return "skip"
    
    return prediction