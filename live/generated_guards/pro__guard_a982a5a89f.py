def guard(features: dict, prediction: str) -> str:
    # Filter longs: require bullish stoch crossover and not overbought
    if prediction == "long":
        if features["stoch_k"] <= features["stoch_d"] or features["stoch_k"] > 70:
            return "skip"
    
    # Filter shorts: require bearish stoch crossover and not oversold
    if prediction == "short":
        if features["stoch_k"] >= features["stoch_d"] or features["stoch_k"] < 30:
            return "skip"
    
    return prediction