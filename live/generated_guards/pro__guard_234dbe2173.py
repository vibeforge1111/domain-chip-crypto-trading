def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (low conviction)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    
    # Skip if stochastic in extreme zones
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    
    return prediction