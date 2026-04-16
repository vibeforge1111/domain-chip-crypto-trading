def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (weak macd_histogram)."""
    if prediction == "skip":
        return prediction
    macd = features.get('macd_histogram', 0)
    # Momentum must align with direction; near-zero indicates deceleration
    if abs(macd) < 0.00005:
        return "skip"
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction