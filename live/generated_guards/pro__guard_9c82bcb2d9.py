def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    # Skip trades too close to fair value (low conviction)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    
    # Skip counter-trend trades at stochastic extremes
    stoch_k = features.get('stoch_k', 50)
    macd = features.get('macd_histogram', 0)
    if stoch_k > 80 and macd < 0:
        return "skip"
    if stoch_k < 20 and macd > 0:
        return "skip"
    
    return prediction