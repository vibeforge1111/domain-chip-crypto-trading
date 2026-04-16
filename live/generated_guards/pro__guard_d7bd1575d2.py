def guard(features: dict, prediction: str) -> str:
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Strong disagreement: price above VWAP but bearish momentum (or vice versa)
    disagreement = vwap_deviation * momentum_score
    
    # Reject if significant disagreement detected
    if disagreement < -0.005:
        return "skip"
    
    # Additional context filter: for longs, require price above VWAP OR strong momentum
    if prediction == "long" and vwap_deviation > 0.002 and momentum_score < -0.3:
        return "skip"
    
    # For shorts, require price below VWAP OR strong momentum
    if prediction == "short" and vwap_deviation < -0.002 and momentum_score > 0.3:
        return "skip"
    
    return prediction