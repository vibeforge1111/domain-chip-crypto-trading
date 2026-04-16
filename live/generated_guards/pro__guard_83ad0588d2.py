def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if vwap_deviation and momentum_score disagree
    # Price above VWAP but negative momentum, or price below VWAP but positive momentum
    if (vwap_dev > 0.005 and momentum < -0.2) or (vwap_dev < -0.005 and momentum > 0.2):
        return "skip"
    
    return prediction