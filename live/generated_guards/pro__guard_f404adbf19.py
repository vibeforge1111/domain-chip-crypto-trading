def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Disagreement: price far below VWAP but momentum is positive
    if vwap_dev < -0.003 and momentum > 0.25:
        return "skip"
    
    # Disagreement: price far above VWAP but momentum is negative
    if vwap_dev > 0.003 and momentum < -0.25:
        return "skip"
    
    # Stochastic confirmation: if stoch confirms vwap/momentum disagreement
    if stoch_k > 80 and stoch_d > 75 and vwap_dev < -0.002 and momentum > 0.2:
        return "skip"
    if stoch_k < 20 and stoch_d < 25 and vwap_dev > 0.002 and momentum < -0.2:
        return "skip"
    
    return prediction