def guard(features: dict, prediction: str) -> str:
    """Filter trades misaligned with 2-hour broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    if prediction == "long" and stoch_k < 20:
        return "skip"
    if prediction == "short" and stoch_k > 80:
        return "skip"
    
    return prediction