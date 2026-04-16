def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (low vwap_deviation)."""
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip if price is too close to fair value (low deviation)
    # Require meaningful deviation from VWAP for trade edge
    if abs(vwap_dev) < 0.005:
        return "skip"
    
    # Additional filter: skip if overbought/oversold extremes align poorly with direction
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction