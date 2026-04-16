def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if too close to VWAP (within 0.3% of price)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Additional filter: avoid trades when 2h RSI is neutral (45-55)
    if 45 < rsi_2h < 55 and abs(vwap_dev) < 0.008:
        return "skip"
    
    return prediction