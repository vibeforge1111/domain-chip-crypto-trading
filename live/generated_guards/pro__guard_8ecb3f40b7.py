def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Bullish crossover: K above D in oversold zone
        if not (stoch_k > stoch_d and stoch_k < 25):
            return "skip"
    
    elif prediction == "short":
        # Bearish crossover: K below D in overbought zone
        if not (stoch_k < stoch_d and stoch_k > 75):
            return "skip"
    
    return prediction