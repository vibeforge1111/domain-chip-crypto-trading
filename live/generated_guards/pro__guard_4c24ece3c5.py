def guard(features: dict, prediction: str) -> str:
    """Filter trades based on Stochastic crossover alignment."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    # Reject longs if not in bullish crossover (k above d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    # Reject shorts if not in bearish crossover (k below d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    return prediction