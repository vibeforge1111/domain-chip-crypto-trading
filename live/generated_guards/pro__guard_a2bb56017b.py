def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (no edge) with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if too close to VWAP (within 0.3% of price)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Validate momentum aligns with direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction