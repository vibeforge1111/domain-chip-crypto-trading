def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    # Skip longs when OBV slope is negative (volume flowing out against long)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    # Skip shorts when OBV slope is positive (volume flowing in against short)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    return prediction