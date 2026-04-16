def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if vwap and momentum strongly disagree
    if (vwap_dev > 0.005 and momentum < -0.5) or (vwap_dev < -0.005 and momentum > 0.5):
        return "skip"
    
    return prediction