def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover momentum alignment."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For longs, require stoch_k above stoch_d (bullish momentum)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For shorts, require stoch_k below stoch_d (bearish momentum)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction