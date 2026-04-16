def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Bullish crossover setup: k crossed above d in oversold zone
        if stoch_k > stoch_d and stoch_k < 30 and stoch_d < 30:
            return prediction
        return "skip"
    
    if prediction == "short":
        # Bearish crossover setup: k crossed below d in overbought zone
        if stoch_k < stoch_d and stoch_k > 70 and stoch_d > 70:
            return prediction
        return "skip"
    
    return prediction