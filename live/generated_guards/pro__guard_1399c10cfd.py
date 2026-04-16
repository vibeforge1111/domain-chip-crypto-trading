def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum deceleration (macd_histogram opposing direction)."""
    if prediction == "long" and features.get("macd_histogram", 0) < -0.0003:
        return "skip"
    if prediction == "short" and features.get("macd_histogram", 0) > 0.0003:
        return "skip"
    if abs(features.get("vwap_deviation", 0)) > 0.015:
        return "skip"
    return prediction