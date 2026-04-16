def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP position and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Price above VWAP but momentum AND stoch weak = skip
    if vwap_dev > 0.015 and momentum < -0.05 and stoch_k < 45:
        return "skip"
    # Price below VWAP but momentum AND stoch strong = skip
    if vwap_dev < -0.015 and momentum > 0.05 and stoch_k > 55:
        return "skip"
    
    return prediction