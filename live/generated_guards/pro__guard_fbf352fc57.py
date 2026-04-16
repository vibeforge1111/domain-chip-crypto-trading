def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0.1)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # False compression: both very low = dead zone with no energy for sustained moves
    if bb_width < 0.025 and atr_ratio < 0.55:
        return "skip"
    return prediction