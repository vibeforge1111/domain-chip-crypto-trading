def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP (< 0.3% from fair value)
    if vwap_dev < 0.003:
        return "skip"
    # Skip momentum conflicts: long in overbought, short in oversold
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    return prediction