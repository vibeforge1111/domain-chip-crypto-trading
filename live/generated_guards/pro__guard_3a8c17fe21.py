def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    
    # Align entries with broader 2h trend
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction