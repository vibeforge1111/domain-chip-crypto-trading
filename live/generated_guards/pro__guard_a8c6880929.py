def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value) with quality checks."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to fair value (within 0.3% of VWAP)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # For longs, skip if stochastics overbought (potential reversal)
    if prediction == "long" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    # For shorts, skip if stochastics oversold (potential bounce)
    if prediction == "short" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction