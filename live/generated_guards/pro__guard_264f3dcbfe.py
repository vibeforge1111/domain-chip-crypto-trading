def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip long if price below VWAP AND momentum negative
    if prediction == "long" and vwap_dev < -0.003 and momentum < 0:
        return "skip"
    
    # Skip short if price above VWAP AND momentum positive
    if prediction == "short" and vwap_dev > 0.003 and momentum > 0:
        return "skip"
    
    return prediction