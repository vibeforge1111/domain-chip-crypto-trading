def guard(features: dict, prediction: str) -> str:
    """Reject trades when RSI contradicts the predicted direction."""
    rsi = features.get("rsi_14", 50)
    
    if prediction == "long" and rsi < 45:
        return "skip"
    if prediction == "short" and rsi > 55:
        return "skip"
    
    return prediction