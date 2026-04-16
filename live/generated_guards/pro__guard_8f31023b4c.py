def guard(features: dict, prediction: str) -> str:
    # Skip if macd_histogram indicates momentum deceleration (near zero)
    if abs(features.get('macd_histogram', 0)) < 0.0001:
        return "skip"
    return prediction