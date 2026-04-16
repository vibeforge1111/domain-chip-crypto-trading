def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing in extreme zones."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Long signals: stoch_k crosses above stoch_d from oversold
    if prediction == "long" and stoch_k < stoch_d and stoch_k > 20:
        return "skip"
    
    # Short signals: stoch_k crosses below stoch_d from overbought
    if prediction == "short" and stoch_k > stoch_d and stoch_k < 80:
        return "skip"
    
    return prediction