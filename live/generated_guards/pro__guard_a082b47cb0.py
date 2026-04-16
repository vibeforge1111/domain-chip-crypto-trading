def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Trend alignment from higher timeframe
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Stochastic crossover confirmation
    # For longs: stoch_k above stoch_d (bullish momentum)
    # For shorts: stoch_k below stoch_d (bearish momentum)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction