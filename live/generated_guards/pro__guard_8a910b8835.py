def guard(features: dict, prediction: str) -> str:
    # Filter trades when price is too close to VWAP (low edge)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip if deviation is too small (within 0.3% of fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if price too close to VWAP AND momentum is weak
    if abs(vwap_dev) < 0.005 and features.get('momentum_score', 0) < 0.3:
        return "skip"
    
    return prediction