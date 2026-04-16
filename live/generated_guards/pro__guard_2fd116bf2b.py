def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating using MACD histogram."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    # Reject long when histogram negative (momentum weakening)
    if prediction == "long" and macd < 0:
        return "skip"
    # Reject short when histogram positive (momentum strengthening)
    if prediction == "short" and macd > 0:
        return "skip"
    # Extra confirmation: overbought/oversold with conflicting momentum
    if prediction == "long" and stoch > 75 and macd < 0:
        return "skip"
    if prediction == "short" and stoch < 25 and macd > 0:
        return "skip"
    return prediction