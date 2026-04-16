def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using RSI."""
    rsi_2h = features.get('rsi_2h', 50)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    return prediction