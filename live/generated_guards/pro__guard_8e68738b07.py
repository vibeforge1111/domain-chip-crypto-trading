def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip when price far below VWAP but momentum bullish and stochastic overbought
    if vwap_dev < -0.015 and momentum > 0.3 and stoch_k > 75:
        return "skip"
    # Skip when price far above VWAP but momentum bearish and stochastic oversold
    if vwap_dev > 0.015 and momentum < -0.3 and stoch_k < 25:
        return "skip"
    
    return prediction