def guard(features: dict, prediction: str) -> str:
    """Filter trades counter to the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and rsi_2h < 30:
        return "skip"
    if prediction == "short" and rsi_2h > 70:
        return "skip"
    return prediction