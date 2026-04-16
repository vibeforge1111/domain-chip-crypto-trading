def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct = features.get('bb_pct_b', 0.5)
    
    # Reject when too close to VWAP (within 0.3%) AND either overbought/oversold extreme
    if abs(vwap_dev) < 0.003 and (stoch_k > 80 or stoch_k < 20):
        return "skip"
    
    # Reject when price near VWAP AND extreme BB position
    if abs(vwap_dev) < 0.002 and (bb_pct > 0.9 or bb_pct < 0.1):
        return "skip"
    
    return prediction