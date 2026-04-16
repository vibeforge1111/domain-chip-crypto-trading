def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if momentum and VWAP position disagree
    if momentum > 0.2 and vwap_dev < -0.003:
        return "skip"
    if momentum < -0.2 and vwap_dev > 0.003:
        return "skip"
    
    return prediction