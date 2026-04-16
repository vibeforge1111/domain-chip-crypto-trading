def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Require volume confirmation
    if volume_ratio < 0.8:
        return "skip"
    
    if prediction == "long":
        if stoch_diff <= 0 or stoch_d > 30:
            return "skip"
    elif prediction == "short":
        if stoch_diff >= 0 or stoch_d < 70:
            return "skip"
    
    return prediction