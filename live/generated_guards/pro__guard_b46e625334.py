def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is misaligned with the predicted direction.
    Uses stochastic crossover and overbought/oversold levels to filter weak setups.
    """
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Reject longs when stochastic shows bearish crossover or overbought
        if stoch_k < stoch_d or stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Reject shorts when stochastic shows bullish crossover or oversold
        if stoch_k > stoch_d or stoch_k < 20:
            return "skip"
    return prediction