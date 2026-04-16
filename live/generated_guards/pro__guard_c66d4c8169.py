def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow."""
    obv = features.get("obv_slope", 0)
    if prediction == "long" and obv < -0.3:
        return "skip"
    if prediction == "short" and obv > 0.3:
        return "skip"
    return prediction