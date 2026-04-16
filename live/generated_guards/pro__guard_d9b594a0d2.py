def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value or with conflicting timeframes."""
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if price is too close to VWAP (within 0.3% either direction)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Also skip longs when 2h RSI is overbought, or shorts when oversold
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction