def guard(features: dict, prediction: str) -> str:
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    disagreement = vwap * momentum
    
    if disagreement < -0.005:
        return "skip"
    
    return prediction