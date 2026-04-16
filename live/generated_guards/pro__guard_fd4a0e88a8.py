def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum vs VWAP disagreement or conflicting stochastic."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Momentum and VWAP disagreement check
    if prediction == "long" and momentum < -0.3 and vwap_dev < -0.005:
        return "skip"
    if prediction == "short" and momentum > 0.3 and vwap_dev > 0.005:
        return "skip"
    
    # Stochastic conflict check
    if prediction == "long" and stoch_k > 85 and stoch_d > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15 and stoch_d < 15:
        return "skip"
    
    return prediction