def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Align short-term signals with broader 2h trend
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction