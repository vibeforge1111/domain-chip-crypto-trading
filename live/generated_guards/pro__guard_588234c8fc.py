def guard(features: dict, prediction: str) -> str:
    """Filter trades misaligned with broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and rsi_2h < 38:
        return "skip"
    if prediction == "short" and rsi_2h > 62:
        return "skip"
    return prediction