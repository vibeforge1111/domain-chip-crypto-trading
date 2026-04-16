def guard(features: dict, prediction: str) -> str:
    # Reject trades when momentum diverges from direction
    hist = features.get("macd_histogram", 0)
    if prediction == "long" and hist < 0:
        return "skip"
    if prediction == "short" and hist > 0:
        return "skip"
    # Momentum deceleration: reject when stoch extremes align with reversal risk
    if features.get("stoch_k", 50) > 85 and features.get("stoch_d", 50) > 80:
        return "skip"
    if features.get("stoch_k", 50) < 15 and features.get("stoch_d", 50) < 20:
        return "skip"
    return prediction