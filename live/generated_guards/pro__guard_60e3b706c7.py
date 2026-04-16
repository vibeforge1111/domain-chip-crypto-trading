def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2h RSI to align entries with broader trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction