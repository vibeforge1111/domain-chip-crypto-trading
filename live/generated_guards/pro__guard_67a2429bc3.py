def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (insufficient deviation from fair value)
    if abs(features.get('vwap_deviation', 0)) < 0.004:
        return "skip"
    return prediction