def guard(features: dict, prediction: str) -> str:
    """Skip trades where vwap_deviation and momentum_score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Price above VWAP but momentum bearish → skip
    if vwap_dev > 0.005 and momentum < -0.1:
        return "skip"
    # Price below VWAP but momentum bullish → skip
    if vwap_dev < -0.005 and momentum > 0.1:
        return "skip"
    
    return prediction