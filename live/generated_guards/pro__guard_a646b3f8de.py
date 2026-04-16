def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get("rsi_2h", 50)
    # For longs: skip if broader 2h RSI is overbought (bullish alignment needed)
    if prediction == "long" and rsi_2h > 68:
        return "skip"
    # For shorts: skip if broader 2h RSI is oversold (bearish alignment needed)
    if prediction == "short" and rsi_2h < 32:
        return "skip"
    return prediction