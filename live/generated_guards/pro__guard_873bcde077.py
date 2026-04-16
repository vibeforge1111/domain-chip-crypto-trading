def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Require bullish alignment for longs
    if prediction == 'long' and (stoch_k <= stoch_d or macd_histogram < 0):
        return 'skip'
    
    # Require bearish alignment for shorts
    if prediction == 'short' and (stoch_k >= stoch_d or macd_histogram > 0):
        return 'skip'
    
    return prediction