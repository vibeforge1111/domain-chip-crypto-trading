def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_14 = features.get("rsi_14", 50)
    
    # For long: require bullish crossover with meaningful separation
    if prediction == "long":
        if stoch_k <= stoch_d or (stoch_k - stoch_d) < 5:
            return "skip"
        if rsi_14 > 70:  # Avoid entries when RSI is already extended
            return "skip"
    
    # For short: require bearish crossover with meaningful separation
    elif prediction == "short":
        if stoch_k >= stoch_d or (stoch_d - stoch_k) < 5:
            return "skip"
        if rsi_14 < 30:  # Avoid shorting into oversold conditions
            return "skip"
    
    return prediction