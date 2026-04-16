def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Price above VWAP but bearish momentum = disagreement
    if vwap_dev > 0.01 and momentum < -0.05:
        return "skip"
    
    # Price below VWAP but bullish momentum = disagreement
    if vwap_dev < -0.01 and momentum > 0.05:
        return "skip"
    
    return prediction