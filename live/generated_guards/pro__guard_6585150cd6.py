def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum_score disagreement."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs: price too far below VWAP but momentum positive (disagreement)
    if prediction == "long" and vwap_dev < -0.015 and momentum > 0.3:
        return "skip"
    
    # Skip shorts: price too far above VWAP but momentum negative (disagreement)
    if prediction == "short" and vwap_dev > 0.015 and momentum < -0.3:
        return "skip"
    
    # Additional filter: skip longs when stoch extremely oversold with negative vwap_dev
    if prediction == "long" and stoch_k < 25 and vwap_dev < -0.01:
        return "skip"
    
    # Additional filter: skip shorts when stoch extremely overbought with positive vwap_dev
    if prediction == "short" and stoch_k > 75 and vwap_dev > 0.01:
        return "skip"
    
    return prediction