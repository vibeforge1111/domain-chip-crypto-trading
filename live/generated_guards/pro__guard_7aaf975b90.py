def guard(features: dict, prediction: str) -> str:
    """Filter trades when broader 2h timeframe contradicts direction."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2h RSI extremely overbought (reversal risk)
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    # Reject shorts when 2h RSI extremely oversold (reversal risk)
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction