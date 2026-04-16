def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    # Skip longs when broader RSI is oversold (<35)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    # Skip shorts when broader RSI is overbought (>65)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    return prediction