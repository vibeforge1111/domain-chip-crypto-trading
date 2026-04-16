def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum_score = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject if price too far from VWAP in wrong direction
    if prediction == "long" and vwap_dev < -0.015:
        return "skip"
    if prediction == "short" and vwap_dev > 0.015:
        return "skip"
    
    # Reject if momentum and stochastic strongly disagree
    if prediction == "long" and momentum_score < 0 and stoch_k < 30:
        return "skip"
    if prediction == "short" and momentum_score > 0 and stoch_k > 70:
        return "skip"
    
    # Reject if 2h RSI conflicts with momentum direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction