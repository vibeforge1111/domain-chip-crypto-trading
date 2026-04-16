def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes with VWAP and momentum confirmation."""
    bb_pct = features.get('bb_pct_b', 0.5)
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Only allow trades in extreme BB zones with aligned confirmation
    in_extreme_zone = bb_pct < 0.05 or bb_pct > 0.95
    near_vwap = abs(vwap_dev) < 0.015
    not_overextended = stoch_k < 85
    
    if in_extreme_zone and near_vwap and not_overextended:
        return prediction
    return "skip"