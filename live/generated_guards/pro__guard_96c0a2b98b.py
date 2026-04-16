def guard(features: dict, prediction: str) -> str:
    """Reject trades when stochastic alignment contradicts momentum direction."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        # Reject if stoch_k below stoch_d (bearish alignment, no momentum confirmation)
        if stoch_k < stoch_d:
            return "skip"
    elif prediction == "short":
        # Reject if stoch_k above stoch_d (bullish alignment, momentum against short)
        if stoch_k > stoch_d:
            return "skip"
    return prediction