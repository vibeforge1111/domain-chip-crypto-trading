def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to fair value (VWAP)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    return prediction