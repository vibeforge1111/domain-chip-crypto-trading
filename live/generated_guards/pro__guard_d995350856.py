def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Reject longs when price far below VWAP with weak/negative momentum
    if prediction == "long" and vwap_dev < -0.01 and momentum < 0:
        return "skip"
    
    # Reject shorts when price far above VWAP with strong/positive momentum
    if prediction == "short" and vwap_dev > 0.01 and momentum > 0:
        return "skip"
    
    return prediction