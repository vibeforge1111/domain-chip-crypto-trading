def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    threshold = 0.001

    # Skip longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -threshold:
        return "skip"

    # Skip shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > threshold:
        return "skip"

    return prediction