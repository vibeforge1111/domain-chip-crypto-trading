def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Disagreement: price above VWAP but momentum bearish
    if vwap_dev > 0.003 and momentum < -0.2:
        return "skip"
    
    # Disagreement: price below VWAP but momentum bullish
    if vwap_dev < -0.003 and momentum > 0.2:
        return "skip"
    
    # Additional filter: stochastic confirms disagreement
    if vwap_dev > 0.003 and stoch_k > 75:
        return "skip"
    if vwap_dev < -0.003 and stoch_k < 25:
        return "skip"
    
    return prediction