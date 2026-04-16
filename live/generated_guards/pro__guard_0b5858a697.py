def guard(features: dict, prediction: str) -> str:
    """Reject trades with volatile moves lacking volume confirmation."""
    high_atr_move = features.get('atr_ratio', 0) > 1.3
    low_volume = features.get('volume_ratio', 1) < 0.7
    
    if high_atr_move and low_volume:
        return "skip"
    
    return prediction