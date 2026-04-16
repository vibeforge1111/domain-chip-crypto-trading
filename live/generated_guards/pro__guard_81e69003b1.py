def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP deviation conflicts with momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    macd = features.get('macd_histogram', 0)
    
    # Price above VWAP but momentum/stochastic bearish → reject
    if vwap_dev > 0.008 and momentum < -0.1 and stoch_k < 40:
        return "skip"
    
    # Price below VWAP but momentum/stochastic bullish → reject
    if vwap_dev < -0.008 and momentum > 0.1 and stoch_k > 60:
        return "skip"
    
    # MACD histogram disagrees with VWAP direction
    if vwap_dev > 0.005 and macd < -0.0002:
        return "skip"
    if vwap_dev < -0.005 and macd > 0.0002:
        return "skip"
    
    return prediction