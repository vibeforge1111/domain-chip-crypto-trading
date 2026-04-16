def guard(features: dict, prediction: str) -> str:
    # True compression: both atr_ratio and bb_width indicate low volatility
    low_atr = features.get('atr_ratio', 1.0) < 0.75
    narrow_bb = features.get('bb_width', 1.0) < 0.35
    
    # Skip trades during true compression (false breakouts likely)
    if low_atr and narrow_bb:
        return "skip"
    
    return prediction