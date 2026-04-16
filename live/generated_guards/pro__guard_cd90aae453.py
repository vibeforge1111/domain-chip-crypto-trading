def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Reject longs when momentum is bearish or price is below VWAP
    if prediction == "long":
        if momentum < 0 or vwap_dev < 0:
            return "skip"
    
    # Reject shorts when momentum is bullish or price is above VWAP
    if prediction == "short":
        if momentum > 0 or vwap_dev > 0:
            return "skip"
    
    return prediction