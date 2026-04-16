def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    sk, sd = features.get("stoch_k", 50), features.get("stoch_d", 50)
    bb_pos = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    
    if prediction == "long":
        # Reject if not bullish crossover or not in lower BB half
        if sk <= sd or bb_pos > 0.5:
            return "skip"
    elif prediction == "short":
        # Reject if not bearish crossover or not in upper BB half
        if sk >= sd or bb_pos < 0.5:
            return "skip"
    
    return prediction