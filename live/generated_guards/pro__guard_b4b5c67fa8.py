def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram contradicts momentum direction."""
    macd = features.get('macd_histogram', 0)
    if prediction == "long" and macd < -0.0001:
        return "skip"
    if prediction == "short" and macd > 0.0001:
        return "skip"
    return prediction