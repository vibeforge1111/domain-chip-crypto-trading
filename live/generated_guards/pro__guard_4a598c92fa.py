def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long":
        # Require stoch_k above stoch_d, not overbought, not at upper band
        if stoch_k <= stoch_d or stoch_k > 80 or bb_pct_b > 0.88:
            return "skip"
    elif prediction == "short":
        # Require stoch_k below stoch_d, not oversold, not at lower band
        if stoch_k >= stoch_d or stoch_k < 20 or bb_pct_b < 0.12:
            return "skip"
    
    return prediction