def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using stochastic crossover."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    if prediction == "long":
        # Reject if overbought zone with bearish crossover
        if stoch_k > 75 and stoch_d > 75 and stoch_diff < 0:
            return "skip"
        # Reject if crossover already occurred far above
        if stoch_diff > 15 and stoch_k > 70:
            return "skip"
    elif prediction == "short":
        # Reject if oversold zone with bullish crossover
        if stoch_k < 25 and stoch_d < 25 and stoch_diff > 0:
            return "skip"
        # Reject if crossover already occurred far below
        if stoch_diff < -15 and stoch_k < 30:
            return "skip"
    
    return prediction