def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    momentum = features.get("momentum_score", 0)
    
    if prediction == "long" and obv_slope < -0.05 and momentum < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0.05 and momentum > 0:
        return "skip"
    
    return prediction