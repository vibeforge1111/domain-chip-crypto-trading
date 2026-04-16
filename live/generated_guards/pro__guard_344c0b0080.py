def guard(features: dict, prediction: str) -> str:
    """Filter trades during low-volume Bollinger Band compression."""
    bb_width = features.get("bb_width", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Skip when BB is narrow (compressed) and volume is low - potential breakout trap
    if bb_width < 0.15 and volume_ratio < 0.7:
        return "skip"
    
    return prediction