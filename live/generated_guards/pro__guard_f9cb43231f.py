def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to VWAP (within 0.3% of fair value)
    if abs(vwap_deviation) < 0.003:
        return "skip"
    
    # Skip if stochastic in extreme territory (overbought >80 or oversold <20)
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    
    return prediction