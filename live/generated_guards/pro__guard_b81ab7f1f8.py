def guard(features: dict, prediction: str) -> str:
    """Filter trades with extreme BB position + RSI divergence (potential reversal zones)."""
    bb_pos = features.get("bb_position", 0.5)
    rsi = features.get("rsi_14", 50)
    
    # Price at upper band with overbought RSI = risky for longs
    if bb_pos > 0.9 and rsi > 70 and prediction == "long":
        return "skip"
    
    # Price at lower band with oversold RSI = risky for shorts
    if bb_pos < 0.1 and rsi < 30 and prediction == "short":
        return "skip"
    
    return prediction