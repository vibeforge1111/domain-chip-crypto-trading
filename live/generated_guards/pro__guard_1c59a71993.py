def guard(features: dict, prediction: str) -> str:
    """Filter signals where dominant wick dominates body (rejection candle)."""
    dominant_wick = max(features['upper_wick_ratio'], features['lower_wick_ratio'])
    if dominant_wick > 0.65 and features['body_ratio'] < 0.25:
        return "skip"
    return prediction