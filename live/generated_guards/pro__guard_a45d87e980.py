def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression without momentum confirmation."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # True compression: tight bands + low ATR
    is_compressed = atr_ratio < 0.6 and bb_width < 0.25
    
    # Momentum needs life (not dead zone, not overheated)
    has_momentum = 15 < stoch_k < 85 and 15 < stoch_d < 85
    
    # Skip if compressed but lacks momentum confirmation
    if is_compressed and not has_momentum:
        return "skip"
    
    return prediction