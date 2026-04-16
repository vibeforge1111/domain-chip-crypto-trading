def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Skip if price is too close to VWAP and near middle of Bollinger Band
    if abs(vwap_dev) < 0.004 and 0.35 < bb_pct_b < 0.65:
        return "skip"
    
    return prediction