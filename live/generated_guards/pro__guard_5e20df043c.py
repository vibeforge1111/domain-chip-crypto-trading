def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP or with conflicting stochastic."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP (within 0.3%)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip long if overbought, short if oversold
    if stoch_k > 85 and prediction == "long":
        return "skip"
    if stoch_k < 15 and prediction == "short":
        return "skip"
    
    return prediction