def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Require bullish stochastic crossover (k above d) for longs
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require bearish stochastic crossover (k below d) for shorts
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Confirm momentum alignment with macd_histogram
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    return prediction