def guard(features: dict, prediction: str) -> str:
    # Skip trades when price is too close to VWAP (within 0.2% either direction)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction