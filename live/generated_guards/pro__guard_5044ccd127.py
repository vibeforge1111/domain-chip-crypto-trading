def guard(features: dict, prediction: str) -> str:
    """Skip signals during compressed markets with conflicting indicators."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.05)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_histogram = features.get('macd_histogram', 0.0)
    vwap_deviation = features.get('vwap_deviation', 0.0)
    
    # True compression: both volatility and bandwidth are low
    is_compression = atr_ratio < 0.7 and bb_width < 0.02
    
    # False compression: extreme price position within tight bands
    extreme_position = bb_pct_b > 0.88 or bb_pct_b < 0.12
    
    # Conflicting momentum: weakening MACD + far from VWAP suggests trap
    weak_momentum = abs(macd_histogram) < 0.0005
    far_from_vwap = abs(vwap_deviation) > 0.015
    
    if is_compression and extreme_position and (weak_momentum or far_from_vwap):
        return "skip"
    
    return prediction