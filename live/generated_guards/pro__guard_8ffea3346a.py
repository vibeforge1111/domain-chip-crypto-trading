def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    sk = features.get("stoch_k", 50)
    sd = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Require bullish crossover (k crosses above d)
        if sk <= sd:
            return "skip"
        # Avoid late entries in overbought territory
        if sk > 85:
            return "skip"
    
    if prediction == "short":
        # Require bearish crossover (k crosses below d)
        if sk >= sd:
            return "skip"
        # Avoid late entries in oversold territory
        if sk < 15:
            return "skip"
    
    return prediction