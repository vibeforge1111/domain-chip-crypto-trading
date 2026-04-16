def guard(features: dict, prediction: str) -> str:
    """Filter signals during Bollinger Band squeeze breakouts at extremes."""
    bb_width = features.get('bb_width', 0.05)
    bb_position = features.get('bb_position', 0.5)
    
    # BB squeeze: narrow bands indicate compression
    is_squeeze = bb_width < 0.02
    
    # Price at band extremes (breakout-prone zones)
    at_extreme = bb_position > 0.92 or bb_position < 0.08
    
    # Skip breakout trades during squeeze conditions
    if is_squeeze and at_extreme:
        return "skip"
    
    return prediction