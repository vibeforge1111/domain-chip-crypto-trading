def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI to align with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long entries: skip if wider timeframe is oversold (potential reversal coming)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    
    # Short entries: skip if wider timeframe is overbought (potential reversal coming)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction