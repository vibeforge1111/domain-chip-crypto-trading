def guard(features: dict, prediction: str) -> str:
    """Filter trades with extreme VWAP deviation and indicator disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Skip if price too far from VWAP (>1.5%)
    if abs(vwap_dev) > 0.015:
        return "skip"
    
    # Skip if stoch and rsi_2h disagree on momentum
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    rsi_extreme = rsi_2h > 70 or rsi_2h < 30
    if stoch_extreme != rsi_extreme:
        return "skip"
    
    return prediction