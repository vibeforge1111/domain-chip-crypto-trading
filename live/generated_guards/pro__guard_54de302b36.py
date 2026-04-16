def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    obv_threshold = 0.5
    if prediction == "long" and obv_slope < -obv_threshold:
        return "skip"
    if prediction == "short" and obv_slope > obv_threshold:
        return "skip"
    return prediction