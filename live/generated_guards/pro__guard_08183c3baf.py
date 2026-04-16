def guard(features: dict, prediction: str) -> str:
    """Filter entries misaligned with broader 2h trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    if prediction == "long" and stoch_k < 25:
        return "skip"
    if prediction == "short" and stoch_k > 75:
        return "skip"
    
    return prediction