def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI extremes and VWAP deviation."""
    rsi = features.get("rsi_14", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long if RSI is deeply overbought and 2h RSI confirms strength
    if prediction == "long" and rsi > 75 and rsi_2h > 60:
        return "skip"
    
    # Skip short if RSI is deeply oversold and 2h RSI confirms weakness
    if prediction == "short" and rsi < 25 and rsi_2h < 40:
        return "skip"
    
    # Skip if too far from VWAP (mean reversion likely)
    if abs(vwap_dev) > 0.012:
        return "skip"
    
    return prediction