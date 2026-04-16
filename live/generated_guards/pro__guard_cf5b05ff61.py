def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long signals: reject if price below VWAP and weak momentum, OR momentum disagrees with stochastic
    if prediction == "long":
        if (vwap_dev < -0.005 and momentum < 0.4) or (momentum > 0.5 and stoch_k < 25):
            return "skip"
    
    # Short signals: reject if price above VWAP and strong momentum, OR momentum disagrees with stochastic
    if prediction == "short":
        if (vwap_dev > 0.005 and momentum > 0.6) or (momentum < 0.5 and stoch_k > 75):
            return "skip"
    
    return prediction