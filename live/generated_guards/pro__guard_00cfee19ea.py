def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Reject longs: price above VWAP but momentum disagrees (weak upside)
    if prediction == "long" and vwap_dev > 0.005 and momentum < -0.3:
        return "skip"
    
    # Reject shorts: price below VWAP but momentum disagrees (weak downside)
    if prediction == "short" and vwap_dev < -0.005 and momentum > 0.3:
        return "skip"
    
    return prediction