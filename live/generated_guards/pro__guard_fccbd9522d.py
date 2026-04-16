def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Strong VWAP deviation but weak momentum (potential reversal setup)
    if vwap_dev > 0.02 and momentum < 0.35:
        return "skip"
    if vwap_dev < -0.02 and momentum > 0.65:
        return "skip"
    
    # Stochastic and momentum disagreement
    if stoch_k > 85 and momentum < 0.4:
        return "skip"
    if stoch_k < 15 and momentum > 0.6:
        return "skip"
    
    # Stochastic divergence (K crossing D in wrong direction)
    if stoch_k < stoch_d - 10 and momentum > 0.6:
        return "skip"
    if stoch_k > stoch_d + 10 and momentum < 0.4:
        return "skip"
    
    return prediction