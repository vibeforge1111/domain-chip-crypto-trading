def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.1)
    vwap_deviation = features.get('vwap_deviation', 0.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: low volatility AND tight bands
    is_true_compression = atr_ratio < 0.75 and bb_width < 0.12
    
    # Reject if not in compression or too far from VWAP
    if prediction != 'skip':
        if not is_true_compression:
            return 'skip'
        if abs(vwap_deviation) > 0.015:
            return 'skip'
    
    return prediction