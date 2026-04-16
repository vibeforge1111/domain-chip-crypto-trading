def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Skip longs when extremely overbought
        if bb_pct > 0.95 and stoch > 80:
            return "skip"
    elif prediction == "short":
        # Skip shorts when extremely oversold
        if bb_pct < 0.05 and stoch < 20:
            return "skip"
    return prediction