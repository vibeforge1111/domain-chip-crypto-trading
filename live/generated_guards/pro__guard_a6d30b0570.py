def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum/stochastic disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Disagreement: price above VWAP but weak momentum + weak stochastic
    if vwap_dev > 0.012 and momentum < 0.35 and stoch_k < 40:
        return "skip"
    
    # Disagreement: price below VWAP but strong momentum + strong stochastic
    if vwap_dev < -0.012 and momentum > 0.65 and stoch_k > 60:
        return "skip"
    
    return prediction