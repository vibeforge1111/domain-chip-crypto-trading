def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    
    # True compression: low volatility AND narrow BBs
    # This indicates energy building for a breakout
    if atr_ratio < 0.7 and bb_width < 0.45:
        return prediction
    
    return "skip"