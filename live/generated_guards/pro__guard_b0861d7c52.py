def guard(features: dict, prediction: str) -> str:
    if prediction == "long" and features.get("macd_histogram", 0) <= 0:
        return "skip"
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction