def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover guard for timing precision."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Require bullish stochastic crossover for longs
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require bearish stochastic crossover for shorts
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Align position with VWAP for confirmation
    if prediction == "long" and vwap_dev < -0.002:
        return "skip"
    if prediction == "short" and vwap_dev > 0.002:
        return "skip"
    
    return prediction