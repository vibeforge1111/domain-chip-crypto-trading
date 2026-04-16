def guard(features: dict, prediction: str) -> str:
    """Filters signals in low-volume volatility spikes and tight BB ranges."""
    volume_ratio = features.get('volume_ratio', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.05)
    
    # Skip if volatility spikes without volume confirmation (potential fakeout)
    if atr_ratio > 1.5 and volume_ratio < 0.8:
        return "skip"
    
    # Skip if BBs are compressed (chop zone, breakout direction uncertain)
    if bb_width < 0.015:
        return "skip"
    
    return prediction