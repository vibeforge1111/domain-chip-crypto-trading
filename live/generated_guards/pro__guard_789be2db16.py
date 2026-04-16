def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Require stoch_k to be aligned with prediction direction
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Reject entries when stochastic is extended (reversal risk)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction