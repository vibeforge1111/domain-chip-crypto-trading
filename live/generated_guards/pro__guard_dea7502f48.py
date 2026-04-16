def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Bullish: stoch_k above stoch_d or crossing up from oversold
        if stoch_k < stoch_d and stoch_k > 30:
            return "skip"
    elif prediction == "short":
        # Bearish: stoch_k below stoch_d or crossing down from overbought
        if stoch_k > stoch_d and stoch_k < 70:
            return "skip"
    return prediction