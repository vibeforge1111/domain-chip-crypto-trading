def guard(features: dict, prediction: str) -> str:
    """Custom guard function using 2-hour RSI for broader trend alignment."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader 2h RSI is overbought (exhausted uptrend)
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    # Skip shorts when broader 2h RSI is oversold (potential bounce zone)
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction