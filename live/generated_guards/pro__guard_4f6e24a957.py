def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compression patterns."""
    bb_width = features.get('bb_width', 0.2)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: low bb_width + low atr_ratio
    is_compression = bb_width < 0.15 and atr_ratio < 0.8
    
    # False compression: middle range during compression
    is_middle_range = 0.35 < bb_pct_b < 0.65
    
    # Weak momentum divergence
    has_weak_momentum = abs(stoch_k - stoch_d) > 10
    
    # Price away from fair value
    price_off_vwap = abs(vwap_deviation) > 0.015
    
    # Skip if compression with mixed signals (false breakout risk)
    if is_compression and is_middle_range and has_weak_momentum and price_off_vwap:
        return "skip"
    
    return prediction