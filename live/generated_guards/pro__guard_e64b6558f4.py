def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # For longs: want positive momentum AND price above VWAP
    if prediction == "long":
        if momentum < 0 and vwap_dev < 0:
            return "skip"
        if momentum < 0 and vwap_dev < -0.001:
            return "skip"
    
    # For shorts: want negative momentum AND price below VWAP
    elif prediction == "short":
        if momentum > 0 and vwap_dev > 0:
            return "skip"
        if momentum > 0 and vwap_dev > 0.001:
            return "skip"
    
    return prediction