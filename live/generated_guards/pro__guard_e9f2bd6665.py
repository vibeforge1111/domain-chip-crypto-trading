def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    return prediction