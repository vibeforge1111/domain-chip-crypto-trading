def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating against the intended direction."""
    macd = features.get('macd_histogram', 0)
    # Momentum deceleration: negative for longs, positive for shorts
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    # Additional confirmation: skip if stochastic confirms exhaustion
    stoch = features.get('stoch_k', 50)
    if prediction == "long" and stoch > 85:
        return "skip"
    if prediction == "short" and stoch < 15:
        return "skip"
    return prediction