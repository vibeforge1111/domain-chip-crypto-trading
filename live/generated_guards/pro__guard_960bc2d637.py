def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction