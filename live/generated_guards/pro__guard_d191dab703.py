def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to fair value (no edge to trade)
    if abs(features.get('vwap_deviation', 0)) < 0.004:
        return "skip"
    return prediction