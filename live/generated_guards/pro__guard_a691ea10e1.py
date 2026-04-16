def guard(features: dict, prediction: str) -> str:
    """Stochastic alignment guard - ensure K and D are aligned with direction."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Require bullish alignment for longs (K above D)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require bearish alignment for shorts (K below D)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction