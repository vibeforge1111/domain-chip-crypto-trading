def guard(features: dict, prediction: str) -> str:
    """Reject trades with large wicks (indecision) AND weak trend alignment."""
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    if total_wick > 0.6:
        return "skip"
    
    if features.get('trend_strength', 0) < 0.25:
        return "skip"
    
    return prediction