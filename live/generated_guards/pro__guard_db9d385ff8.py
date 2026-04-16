def guard(features: dict, prediction: str) -> str:
    """Reject trades when stochastic crossover occurs in neutral zone."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Crossover only reliable in oversold (<30) or overbought (>70) zones
    in_oversold = stoch_k < 30 and stoch_d < 30
    in_overbought = stoch_k > 70 and stoch_d > 70
    
    if not (in_oversold or in_overbought):
        return "skip"
    
    return prediction