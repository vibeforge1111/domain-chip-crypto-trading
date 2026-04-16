def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entry filtering."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Require bullish crossover for long entries
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require bearish crossover for short entries
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Skip entries at extreme overbought/oversold levels (exhaustion risk)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction