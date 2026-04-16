def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (no meaningful deviation from fair value)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction