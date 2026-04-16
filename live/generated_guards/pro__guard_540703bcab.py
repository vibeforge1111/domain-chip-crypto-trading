def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_14 = features.get('rsi_14', 50)
    
    # Skip if too close to VWAP (< 0.3% deviation from fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Reject longs in overbought or shorts in oversold
    if prediction == "long" and rsi_14 > 70:
        return "skip"
    if prediction == "short" and rsi_14 < 30:
        return "skip"
    
    return prediction