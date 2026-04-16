def guard(features: dict, prediction: str) -> str:
    # Skip signals when candle shows rejection pattern (large wick + small body)
    dominant_wick = max(features.get('upper_wick_ratio', 0), features.get('lower_wick_ratio', 0))
    if dominant_wick > 0.5 and features.get('body_ratio', 1) < 0.3:
        return "skip"
    return prediction