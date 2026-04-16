def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum is decelerating before entry."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    momentum_score = features.get('momentum_score', 0)
    
    # Skip if stochastic overbought with flattening/weakening MACD momentum
    if stoch_k > 80 and macd_histogram < 0.001:
        return "skip"
    
    # Skip if strong momentum divergence (positive histogram but negative score)
    if macd_histogram > 0 and momentum_score < -0.3:
        return "skip"
    
    return prediction