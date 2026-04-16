def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2h RSI."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        if rsi_2h < 35:
            return "skip"
        if stoch_k < 20:
            return "skip"
    elif prediction == "short":
        if rsi_2h > 65:
            return "skip"
        if stoch_k > 80:
            return "skip"
    
    return prediction