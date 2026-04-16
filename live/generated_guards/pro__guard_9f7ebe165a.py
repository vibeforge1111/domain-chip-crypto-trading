def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with weak confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to VWAP and stochastic confirms exhaustion
    if abs(vwap_dev) < 0.004:
        if (prediction == "long" and stoch_k < 25) or (prediction == "short" and stoch_k > 75):
            return "skip"
    return prediction