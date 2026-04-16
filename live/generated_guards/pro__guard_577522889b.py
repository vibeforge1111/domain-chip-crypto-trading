def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Stochastic crossover alignment
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 80:
            return "skip"
        if bb_pct_b > 0.85:
            return "skip"
        if vwap_deviation > 0.015:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 20:
            return "skip"
        if bb_pct_b < 0.15:
            return "skip"
        if vwap_deviation < -0.015:
            return "skip"
    
    return prediction