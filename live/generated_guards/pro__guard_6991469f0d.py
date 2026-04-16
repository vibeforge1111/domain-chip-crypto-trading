def guard(features: dict, prediction: str) -> str:
    macd = features.get("macd_histogram", 0)
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction