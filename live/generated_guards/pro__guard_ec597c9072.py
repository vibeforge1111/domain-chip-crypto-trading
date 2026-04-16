def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip if too close to fair value (< 0.15%) AND momentum exhausted
    if abs(vwap_dev) < 0.0015 and (stoch_k > 80 or stoch_k < 20 or macd_hist * vwap_dev < 0):
        return "skip"
    return prediction