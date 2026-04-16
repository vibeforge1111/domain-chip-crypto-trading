def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long when below VWAP, negative momentum, and weak stochastic
    if prediction == "long" and vwap_dev < -0.005 and momentum < 0 and stoch_k < 40:
        return "skip"
    
    # Skip short when above VWAP, positive momentum, and strong stochastic
    if prediction == "short" and vwap_dev > 0.005 and momentum > 0 and stoch_k > 60:
        return "skip"
    
    return prediction