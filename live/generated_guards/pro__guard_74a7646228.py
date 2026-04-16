def guard(features: dict, prediction: str) -> str:
    """Filter trades that are too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pos = features.get('bb_pct_b', 0.5)
    
    # Skip if price is too close to VWAP (< 0.3%) while in middle of Bollinger Bands
    if abs(vwap_dev) < 0.003 and 0.3 < bb_pos < 0.7:
        return "skip"
    
    return prediction