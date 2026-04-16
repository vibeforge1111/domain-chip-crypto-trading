def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if too close to VWAP (no reversion edge)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Reject counter-trend trades at extremes
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction