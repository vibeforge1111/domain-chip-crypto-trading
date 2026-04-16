def guard(features: dict, prediction: str) -> str:
    """Filter trades using combined BB position and Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Skip long when both oversold (bad entry timing)
        if bb_pct_b < 0.15 and stoch_k < 20:
            return "skip"
    elif prediction == "short":
        # Skip short when both overbought (bad entry timing)
        if bb_pct_b > 0.85 and stoch_k > 80:
            return "skip"
    
    return prediction