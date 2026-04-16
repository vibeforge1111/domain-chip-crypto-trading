def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram indicates momentum loss or reversal."""
    macd = features.get('macd_histogram', 0)
    # Skip if momentum is negligible (histogram near zero)
    if abs(macd) < 0.0001:
        return "skip"
    # Skip long if histogram is negative (downward momentum)
    if prediction == "long" and macd < 0:
        return "skip"
    # Skip short if histogram is positive (upward momentum)
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction