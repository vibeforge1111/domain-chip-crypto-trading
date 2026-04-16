def guard(features: dict, prediction: str) -> str:
    """Reject trades against OBV volume flow direction."""
    obv = features.get("obv_slope", 0)
    if prediction == "long" and obv < -0.01:
        return "skip"
    if prediction == "short" and obv > 0.01:
        return "skip"
    return prediction