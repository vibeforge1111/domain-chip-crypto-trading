def guard(features: dict, prediction: str) -> str:
    """Filter trades with dominant wicks at extreme BB positions (reversal traps)."""
    dominant_wick = max(features.get('upper_wick_ratio', 0), features.get('lower_wick_ratio', 0))
    bb_extreme = features.get('bb_position', 0.5) < 0.15 or features.get('bb_position', 0.5) > 0.85
    
    if dominant_wick > 0.5 and bb_extreme:
        return "skip"
    
    return prediction