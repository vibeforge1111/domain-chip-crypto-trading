def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    if prediction == "long" and obv_slope < -0.0005:
        return "skip"
    if prediction == "short" and obv_slope > 0.0005:
        return "skip"
    return prediction