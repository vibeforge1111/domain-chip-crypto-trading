def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Price below VWAP but momentum bearish = disagreement
    if vwap_dev < -0.005 and momentum < -0.1:
        return "skip"
    
    # Price above VWAP but momentum bullish = disagreement
    if vwap_dev > 0.005 and momentum > 0.1:
        return "skip"
    
    return prediction