def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI and trend alignment."""
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Skip if RSI neutral (no clear momentum) and low body ratio (doji-like candle)
    if 45 <= rsi <= 55 and body_ratio < 0.4:
        return "skip"
    
    # Longs: require RSI > 50 and upward slope (or at least not strongly downward)
    if prediction == "long" and rsi < 45:
        return "skip"
    
    # Shorts: require RSI < 50 and downward slope (or at least not strongly upward)
    if prediction == "short" and rsi > 55:
        return "skip"
    
    return prediction