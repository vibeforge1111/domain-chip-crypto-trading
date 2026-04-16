def guard(features: dict, prediction: str) -> str:
    # Stochastic crossover timing guard
    # For longs: require stoch_k above stoch_d (bullish crossover) with stoch_d in oversold zone
    # For shorts: require stoch_k below stoch_d (bearish crossover) with stoch_k in overbought zone
    if prediction == "long":
        if features["stoch_k"] <= features["stoch_d"] or features["stoch_d"] > 30:
            return "skip"
    elif prediction == "short":
        if features["stoch_k"] >= features["stoch_d"] or features["stoch_k"] < 70:
            return "skip"
    return prediction