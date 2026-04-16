def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for entry precision."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Check stochastic alignment with prediction direction
    if prediction == "long":
        # For longs: stoch_k should be above stoch_d (bullish alignment)
        # AND not deeply overbought (room to run)
        if stoch_k <= stoch_d and stoch_k > 70:
            return "skip"
    elif prediction == "short":
        # For shorts: stoch_k should be below stoch_d (bearish alignment)
        # AND not deeply oversold (room to fall)
        if stoch_k >= stoch_d and stoch_k < 30:
            return "skip"
    
    return prediction