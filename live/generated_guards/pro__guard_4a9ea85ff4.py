def guard(features: dict, prediction: str) -> str:
    """Skip trades when 2-hour broader RSI contradicts the prediction."""
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long" and rsi_2h < 48:
        return "skip"
    if prediction == "short" and rsi_2h > 52:
        return "skip"
    
    return prediction