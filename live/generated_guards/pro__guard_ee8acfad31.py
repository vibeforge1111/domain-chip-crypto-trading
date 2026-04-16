def guard(features: dict, prediction: str) -> str:
    # Reject candles dominated by wicks (indecision/rejection signals)
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    if total_wick > 0.6:
        return "skip"
    
    # Reject small body candles with low volume (weak conviction)
    body_ratio = features.get('body_ratio', 0)
    volume_ratio = features.get('volume_ratio', 0)
    if body_ratio < 0.25 and volume_ratio < 0.7:
        return "skip"
    
    return prediction