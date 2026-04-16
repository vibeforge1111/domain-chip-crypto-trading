def guard(features: dict, prediction: str) -> str:
    """Reject trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if momentum and VWAP have opposite signs (disagreement)
    if vwap_dev * momentum < 0:
        return "skip"
    
    # Long requires both positive; short requires both negative
    if prediction == "long" and (vwap_dev <= 0 or momentum <= 0):
        return "skip"
    if prediction == "short" and (vwap_dev >= 0 or momentum >= 0):
        return "skip"
    
    return prediction