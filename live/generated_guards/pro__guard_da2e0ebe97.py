def guard(features: dict, prediction: str) -> str:
    """Custom guard function using rsi_2h to align entries with broader trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when 2h RSI is deeply overbought (broader trend exhausted)
    if prediction == "long" and rsi_2h > 78:
        return "skip"
    
    # Skip shorts when 2h RSI is deeply oversold (broader trend exhausted)  
    if prediction == "short" and rsi_2h < 22:
        return "skip"
    
    return prediction