def guard(features: dict, prediction: str) -> str:
    """Reject false compression: tight ATR+BB but weak momentum buildup."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: low ATR + narrow BBs
    compressed = atr_ratio < 0.8 and bb_width < 0.4
    
    if compressed:
        # Mid-range BB suggests indecision
        if 0.25 < bb_pct_b < 0.75:
            return "skip"
        
        # Weak momentum on all indicators confirms false compression
        if abs(macd_histogram) < 0.0001 and obv_slope < 0.05 and abs(rsi_14 - rsi_2h) < 10:
            return "skip"
    
    return prediction