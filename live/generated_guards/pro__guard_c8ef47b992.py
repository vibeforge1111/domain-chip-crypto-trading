def guard(features: dict, prediction: str) -> str:
    """Filter trades based on wick dominance and volume confirmation.
    
    Pin bars and dojis with dominant wicks and low volume are unreliable.
    """
    dominant_wick = max(features.get('upper_wick_ratio', 0), features.get('lower_wick_ratio', 0))
    
    # Strong wick dominance suggests rejection/consolidation, skip if low volume
    if dominant_wick > 0.5 and features.get('volume_ratio', 1) < 1.0:
        return "skip"
    
    return prediction