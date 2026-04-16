def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to fair value (within 0.25% of VWAP)
    # AND stochastics in neutral zone (no strong momentum)
    if abs(vwap_dev) < 0.0025 and 35 < stoch_k < 65:
        return "skip"
    return prediction