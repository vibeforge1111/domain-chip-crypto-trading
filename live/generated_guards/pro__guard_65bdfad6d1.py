def guard(features: dict, prediction: str) -> str:
    """Filter trades when 2-hour RSI contradicts the trade direction."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when 2h RSI shows bearish signal (counter-trend)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Skip shorts when 2h RSI shows bullish signal (counter-trend)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction