def guard(features: dict, prediction: str) -> str:
    """Filter trades using broader timeframe RSI alignment."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when broader timeframe is oversold (bearish pressure)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    
    # Skip shorts when broader timeframe is overbought (bullish pressure)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction