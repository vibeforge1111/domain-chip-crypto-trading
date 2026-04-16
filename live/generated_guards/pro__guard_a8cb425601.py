def guard(features: dict, prediction: str) -> str:
    # Skip if momentum contradicts the signal direction
    hist = features.get('macd_histogram', 0)
    if prediction == "long" and hist < 0:
        return "skip"
    if prediction == "short" and hist > 0:
        return "skip"
    return prediction