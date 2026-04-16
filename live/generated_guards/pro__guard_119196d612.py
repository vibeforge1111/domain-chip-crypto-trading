def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2h trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long" and (rsi_2h < 40 or stoch_k > 80):
        return "skip"
    
    if prediction == "short" and (rsi_2h > 60 or stoch_k < 20):
        return "skip"
    
    return prediction