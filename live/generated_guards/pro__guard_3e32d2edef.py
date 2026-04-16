def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return "skip"
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    rsi_14 = features.get("rsi_14", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # For longs: stochastic bullish crossover from oversold territory
    if prediction == "long":
        if stoch_diff <= 0:
            return "skip"
        if stoch_k > 45 or rsi_14 > 55:
            return "skip"
    
    # For shorts: stochastic bearish crossover from overbought territory
    if prediction == "short":
        if stoch_diff >= 0:
            return "skip"
        if stoch_k < 55 or rsi_14 < 45:
            return "skip"
    
    return prediction