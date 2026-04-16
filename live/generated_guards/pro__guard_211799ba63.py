def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram contradicts momentum direction."""
    if prediction == "long" and features["macd_histogram"] < -0.0002:
        return "skip"
    if prediction == "short" and features["macd_histogram"] > 0.0002:
        return "skip"
    return prediction