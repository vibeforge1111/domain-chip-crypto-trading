def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Price above VWAP but momentum and stoch bearish → disagreement
    if vwap_dev > 0.005 and momentum < -0.15 and stoch_k < 35:
        return "skip"
    
    # Price below VWAP but momentum and stoch bullish → disagreement
    if vwap_dev < -0.005 and momentum > 0.15 and stoch_k > 65:
        return "skip"
    
    return prediction