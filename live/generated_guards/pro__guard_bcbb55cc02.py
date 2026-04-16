def guard(features: dict, prediction: str) -> str:
    # Skip if momentum is decelerating (macd_histogram negative indicates weakening)
    if features.get('macd_histogram', 0) < 0:
        return "skip"
    return prediction