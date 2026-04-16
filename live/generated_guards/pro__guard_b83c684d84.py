def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv = features.get("obv_slope", 0)
    if prediction == "long" and obv < -0.001:
        return "skip"
    if prediction == "short" and obv > 0.001:
        return "skip"
    return prediction