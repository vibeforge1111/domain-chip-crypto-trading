def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating (weak/near-zero macd_histogram)."""
    # Reject if momentum is fading (histogram too close to zero indicates weak momentum)
    if abs(features.get('macd_histogram', 0)) < 0.0002:
        return "skip"
    # Additionally skip if stochastic is extreme and macd histogram opposes the trade direction
    stoch = features.get('stoch_k', 50)
    hist = features.get('macd_histogram', 0)
    if prediction == "long" and stoch > 80 and hist < 0:
        return "skip"
    if prediction == "short" and stoch < 20 and hist > 0:
        return "skip"
    return prediction