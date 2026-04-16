def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # For long, require bullish crossover in oversold zone (<30)
        if stoch_k <= stoch_d or stoch_k >= 30:
            return "skip"
    elif prediction == "short":
        # For short, require bearish crossover in overbought zone (>70)
        if stoch_k >= stoch_d or stoch_k <= 70:
            return "skip"
    
    return prediction