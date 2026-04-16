def guard(features: dict, prediction: str) -> str:
    """Skip trades when OBV slope contradicts prediction direction."""
    obv_slope = features.get('obv_slope', 0)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    return prediction