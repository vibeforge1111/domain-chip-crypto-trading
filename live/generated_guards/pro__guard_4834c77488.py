def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For long entries, require bullish crossover (k above d) in oversold zone
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_d > 40:
            return "skip"
    
    # For short entries, require bearish crossover (k below d) in overbought zone
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_d < 60:
            return "skip"
    
    return prediction