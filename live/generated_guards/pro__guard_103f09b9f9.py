def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Filter if strong disagreement between VWAP position and momentum
    if vwap_dev * momentum < -0.015:
        return "skip"
    
    return prediction