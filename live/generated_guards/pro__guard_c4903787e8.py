def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    
    # Skip if within 0.3% of VWAP AND stochastic at extreme
    if abs(vwap_dev) < 0.003 and (stoch > 80 or stoch < 20):
        return "skip"
    return prediction