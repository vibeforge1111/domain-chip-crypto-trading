def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    # Skip longs when OBV is in distribution phase (negative slope)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    # Skip shorts when OBV is in accumulation phase (positive slope)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    return prediction