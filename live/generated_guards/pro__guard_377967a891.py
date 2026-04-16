def guard(features: dict, prediction: str) -> str:
    vwap_deviation = features.get('vwap_deviation', 0)
    # Skip trades too close to fair value (within 0.2% of price)
    if abs(vwap_deviation) < 0.002:
        return "skip"
    return prediction