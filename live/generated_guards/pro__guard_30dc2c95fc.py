def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating based on macd_histogram."""
    # Skip if momentum histogram is negative (deceleration)
    if features.get('macd_histogram', 0) < -0.0003:
        return "skip"
    # Skip if VWAP deviates significantly against trend direction
    if prediction == "long" and features.get('vwap_deviation', 0) < -0.015:
        return "skip"
    if prediction == "short" and features.get('vwap_deviation', 0) > 0.015:
        return "skip"
    # Skip if stochastics extreme and macd not confirming
    if features.get('stoch_k', 50) > 80 and features.get('macd_histogram', 0) < 0:
        return "skip"
    if features.get('stoch_k', 50) < 20 and features.get('macd_histogram', 0) > 0:
        return "skip"
    return prediction