def guard(features: dict, prediction: str) -> str:
    # Skip if MACD histogram is negative (momentum decelerating/bearish)
    if features.get("macd_histogram", 0) < 0:
        return "skip"
    return prediction