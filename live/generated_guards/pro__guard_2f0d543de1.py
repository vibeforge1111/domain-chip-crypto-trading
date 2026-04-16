def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters entries not at momentum inflection points."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    if prediction == "long":
        # Stochastic bullish crossover: k crosses above d in oversold zone
        if stoch_diff < 2 and stoch_k > stoch_d and stoch_k < 30:
            return prediction
        return "skip"
    
    if prediction == "short":
        # Stochastic bearish crossover: k crosses below d in overbought zone
        if stoch_diff > -2 and stoch_k < stoch_d and stoch_k > 70:
            return prediction
        return "skip"
    
    return prediction