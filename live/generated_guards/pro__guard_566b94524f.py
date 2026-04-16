def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (within 0.3% of price)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    return prediction