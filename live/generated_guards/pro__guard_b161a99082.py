def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters trades without confirming crossover."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long entries require bullish stochastic crossover (k above d)
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    
    # Short entries require bearish stochastic crossover (k below d)
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    return prediction