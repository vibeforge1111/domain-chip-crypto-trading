def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation and consolidation signals."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Filter when price is very close to VWAP (consolidation zone)
    near_fair_value = abs(vwap_dev) < 0.003
    
    # Additional consolidation check: stoch in middle range, BB in middle
    consolidation = (30 < stoch_k < 70) and (30 < stoch_d < 70) and (0.35 < bb_pct_b < 0.65)
    
    # RSI 2H neutral (not trending)
    neutral_2h = 40 < rsi_2h < 60
    
    if near_fair_value and consolidation and neutral_2h:
        return "skip"
    
    return prediction