def guard(features: dict, prediction: str) -> str:
    """Filter trades by aligning with broader 2-hour trend context."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when broader timeframe is oversold (rsi_2h < 35)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    
    # Skip shorts when broader timeframe is overbought (rsi_2h > 65)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction