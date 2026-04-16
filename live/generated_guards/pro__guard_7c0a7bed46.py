def guard(features: dict, prediction: str) -> str:
    """Custom guard function using rsi_2h to align entries with broader trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # For longs: ensure broader 2h trend isn't overbought (rsi_2h > 65)
    if prediction == "long" and rsi_2h > 65:
        return "skip"
    
    # For shorts: ensure broader 2h trend isn't oversold (rsi_2h < 35)
    if prediction == "short" and rsi_2h < 35:
        return "skip"
    
    return prediction