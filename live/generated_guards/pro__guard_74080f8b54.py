def guard(features: dict, prediction: str) -> str:
    # Filter trades where price is too close to fair value (VWAP)
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.0005:  # within 0.05% of VWAP
        return "skip"
    return prediction