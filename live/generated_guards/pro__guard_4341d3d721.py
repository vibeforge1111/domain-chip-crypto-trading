def guard(features: dict, prediction: str) -> str:
    """Filter signals at extreme BB position with doji and high volume (reversal risk)."""
    bb_pos = features.get('bb_position', 0.5)
    body_ratio = features.get('body_ratio', 0.5)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # At extremes with doji and high volume = reversal risk
    at_extreme = bb_pos < 0.15 or bb_pos > 0.85
    is_doji = body_ratio < 0.3
    high_volume = volume_ratio > 1.5
    
    if at_extreme and is_doji and high_volume:
        return "skip"
    
    return prediction