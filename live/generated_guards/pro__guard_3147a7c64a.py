def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    # Skip long if OBV is falling (distribution), skip short if OBV is rising (accumulation)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    return prediction