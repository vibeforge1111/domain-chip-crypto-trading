def guard(features: dict, prediction: str) -> str:
    """Filter trades when RSI is extreme at band extremes - reversal signals."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    bb_pos = features.get("bb_position", 0.5)
    
    # Skip longs when overbought at upper band (potential reversal)
    if prediction == "long" and rsi > 70 and bb_pos > 0.85:
        return "skip"
    
    # Skip shorts when oversold at lower band (potential reversal)
    if prediction == "short" and rsi < 30 and bb_pos < 0.15:
        return "skip"
    
    return prediction