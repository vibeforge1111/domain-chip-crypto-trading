def guard(features: dict, prediction: str) -> str:
    """Guard: align entries with broader trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # In broader uptrend (rsi_2h > 55), reject shorts
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # In broader downtrend (rsi_2h < 45), reject longs
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    return prediction