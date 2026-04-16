def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get("rsi_2h", 50)
    # Align long entries with bullish 2h context
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    # Align short entries with bearish 2h context
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    return prediction