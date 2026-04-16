def guard(features: dict, prediction: str) -> str:
    """Filter trades in false compression setups."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0.0)
    
    # True compression: low atr + low bb_width
    is_compressed = atr_ratio < 0.7 and bb_width < 0.3
    
    # False compression: compressed but price at extreme or far from VWAP
    if is_compressed:
        extreme_position = bb_pct_b > 0.85 or bb_pct_b < 0.15
        far_from_vwap = abs(vwap_dev) > 0.015
        if extreme_position or far_from_vwap:
            return "skip"
    
    return prediction