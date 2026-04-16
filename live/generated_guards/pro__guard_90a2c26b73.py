def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for entry precision."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    ema_slope = features.get("ema_slope", 0)
    
    # Skip longs when both oscillators are overbought (stochastic extreme)
    if prediction == "long" and stoch_k > 75 and stoch_d > 75:
        return "skip"
    
    # Skip shorts when both oscillators are oversold (stochastic extreme)
    if prediction == "short" and stoch_k < 25 and stoch_d < 25:
        return "skip"
    
    # Ensure momentum aligns with trend direction
    if prediction == "long" and ema_slope < -0.001:
        return "skip"
    
    if prediction == "short" and ema_slope > 0.001:
        return "skip"
    
    return prediction