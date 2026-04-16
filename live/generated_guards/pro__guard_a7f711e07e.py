def guard(features: dict, prediction: str) -> str:
    vwap_dev = abs(features.get('vwap_deviation', 0))
    if vwap_dev < 0.004:
        return "skip"
    return prediction