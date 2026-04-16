def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch = features.get('stoch_k', 50)
    
    # Price above VWAP but momentum weak and stochastic not bullish
    if vwap_dev > 0.005 and momentum < -0.1 and stoch < 60:
        return "skip"
    # Price below VWAP but momentum strong and stochastic not bearish
    if vwap_dev < -0.005 and momentum > 0.1 and stoch > 40:
        return "skip"
    
    return prediction