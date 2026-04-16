def guard(features: dict, prediction: str) -> str:
    """Filter signals using RSI and Bollinger Band position interaction."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    
    # Skip longs at overbought levels near upper BB
    if prediction == "long" and rsi > 70 and bb_pos > 0.8:
        return "skip"
    # Skip shorts at oversold levels near lower BB
    if prediction == "short" and rsi < 30 and bb_pos < 0.2:
        return "skip"
    
    return prediction