def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip if stochastic in extreme territory (unreliable crossover signals)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    # Validate crossover direction matches prediction
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        # Require price above VWAP for long entries
        if vwap_deviation < 0:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        # Require price below VWAP for short entries
        if vwap_deviation > 0:
            return "skip"
    
    return prediction