def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if near VWAP (within 0.3%) AND stoch in neutral zone (ranging)
    if abs(vwap_dev) < 0.003 and 30 < stoch_k < 70:
        return "skip"
    return prediction