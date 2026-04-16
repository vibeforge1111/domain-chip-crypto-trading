def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    # Skip longs when price below VWAP and momentum bearish, or shorts when price above VWAP and momentum bullish
    if prediction == "long" and momentum < -0.1 and vwap_dev < -0.005:
        return "skip"
    if prediction == "short" and momentum > 0.1 and vwap_dev > 0.005:
        return "skip"
    return prediction