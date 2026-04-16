def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch = features.get('stoch_k', 50)
    
    # Disagreement: price far from VWAP but momentum contradicts direction
    if vwap_dev > 0.008 and momentum < -0.2:
        return "skip"
    if vwap_dev < -0.008 and momentum > 0.2:
        return "skip"
    
    # Strong momentum with extreme stochastic warns of reversal
    if momentum > 0.6 and stoch > 85:
        return "skip"
    if momentum < -0.6 and stoch < 15:
        return "skip"
    
    return prediction