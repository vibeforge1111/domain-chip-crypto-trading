def guard(features: dict, prediction: str) -> str:
    if abs(features['vwap_deviation']) < 0.005:
        return "skip"
    return prediction