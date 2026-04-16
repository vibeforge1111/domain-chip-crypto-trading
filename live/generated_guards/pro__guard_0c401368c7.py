def guard(features: dict, prediction: str) -> str:
    """Filter trades where candle structure suggests weak momentum."""
    # High wick in direction opposite to prediction signals rejection
    if prediction == "long" and features['upper_wick_ratio'] > 0.5:
        return "skip"
    if prediction == "short" and features['lower_wick_ratio'] > 0.5:
        return "skip"
    return prediction