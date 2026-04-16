def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value with stoch confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if within 0.3% of VWAP and not at stochastic extreme
    if abs(vwap_dev) < 0.003 and not (stoch_k < 20 or stoch_k > 80):
        return "skip"
    return prediction