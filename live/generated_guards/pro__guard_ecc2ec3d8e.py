def guard(features: dict, prediction: str) -> str:
    """Filter entries not aligned with broader trend (rsi_2h) and extreme momentum."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long" and (rsi_2h < 50 or stoch_k > 80):
        return "skip"
    if prediction == "short" and (rsi_2h > 50 or stoch_k < 20):
        return "skip"
    
    return prediction