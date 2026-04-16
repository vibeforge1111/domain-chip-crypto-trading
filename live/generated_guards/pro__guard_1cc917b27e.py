def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    spread = abs(stoch_k - stoch_d)
    
    # Reject countertrend trades at extremes
    if prediction == "long" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    # Require clear crossover momentum (spread > 5)
    if spread < 5:
        return "skip"
    
    # Verify direction aligns with crossover
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction