def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compression patterns."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low bb_width AND low atr_ratio
    is_true_compression = bb_width < 0.25 and atr_ratio < 0.6
    
    if is_true_compression and prediction != "skip":
        # False compression: extreme BB position with significant VWAP deviation
        extreme_position = bb_pct_b < 0.15 or bb_pct_b > 0.85
        vwap_misalignment = abs(vwap_deviation) > 0.01
        
        if extreme_position and vwap_misalignment:
            return "skip"
    
    return prediction