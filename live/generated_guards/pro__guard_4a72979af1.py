def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require meaningful gap for valid crossover signal
    if abs(stoch_k - stoch_d) < 5:
        return "skip"
    
    # Long: stoch_k should be below stoch_d (pre-cross for bullish reversal)
    if prediction == "long":
        return prediction if stoch_k < stoch_d else "skip"
    
    # Short: stoch_k should be above stoch_d (pre-cross for bearish reversal)
    if prediction == "short":
        return prediction if stoch_k > stoch_d else "skip"
    
    return prediction