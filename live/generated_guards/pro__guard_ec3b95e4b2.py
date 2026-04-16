def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if price is too close to fair value (VWAP deviation < 0.2%)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip if stochastic is in extreme overbought/oversold territory
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction