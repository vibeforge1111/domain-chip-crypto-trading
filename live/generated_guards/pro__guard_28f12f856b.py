def guard(features: dict, prediction: str) -> str:
    """Filter trades where broader 2h RSI contradicts direction."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when 2h RSI deeply overbought (likely reversal ahead)
    if prediction == "long" and rsi_2h > 78:
        return "skip"
    
    # Skip shorts when 2h RSI deeply oversold (likely reversal ahead)
    if prediction == "short" and rsi_2h < 22:
        return "skip"
    
    return prediction