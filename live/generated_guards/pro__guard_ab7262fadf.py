def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Price above VWAP but bearish momentum
    if vwap_dev > 0.005 and momentum < -0.25:
        return "skip"
    
    # Price below VWAP but bullish momentum
    if vwap_dev < -0.005 and momentum > 0.25:
        return "skip"
    
    # Stochastic divergence from VWAP signal
    if stoch_k < 20 and vwap_dev > 0.005:
        return "skip"
    if stoch_k > 80 and vwap_dev < -0.005:
        return "skip"
    
    return prediction