def guard(features: dict, prediction: str) -> str:
    # Skip long entries when MACD histogram shows bearish deceleration
    if prediction == "long" and features.get('macd_histogram', 0) < 0:
        return "skip"
    # Skip short entries when MACD histogram shows bullish deceleration
    if prediction == "short" and features.get('macd_histogram', 0) > 0:
        return "skip"
    # Additional momentum filter: skip if extreme stochastics contradict direction
    if features.get('stoch_k', 50) > 80 and prediction == "long":
        return "skip"
    if features.get('stoch_k', 50) < 20 and prediction == "short":
        return "skip"
    return prediction