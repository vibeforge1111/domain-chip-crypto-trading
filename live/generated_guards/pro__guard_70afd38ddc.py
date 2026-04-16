def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP (fair value) with confirmation from stoch."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter: if price within 0.5% of VWAP and stochastic neutral (not extreme)
    if abs(vwap_dev) < 0.005 and 30 <= stoch_k <= 70:
        return "skip"
    return prediction