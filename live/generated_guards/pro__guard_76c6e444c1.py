def guard(features: dict, prediction: str) -> str:
    """Guard against trades with extreme wicks indicating rejection."""
    if prediction == "long" and features.get("upper_wick_ratio", 0) > 0.4:
        return "skip"
    if prediction == "short" and features.get("lower_wick_ratio", 0) > 0.4:
        return "skip"
    if prediction == "long" and features.get("ema_slope", 0) < 0:
        return "skip"
    if prediction == "short" and features.get("ema_slope", 0) > 0:
        return "skip"
    return prediction