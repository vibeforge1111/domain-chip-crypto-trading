def guard(features: dict, prediction: str) -> str:
    # True compression: both atr_ratio AND bb_width are low (squeeze)
    # False compression: price at extreme BB position during squeeze
    in_compression = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 1) < 0.7
    
    if in_compression:
        bb_extreme = features.get('bb_pct_b', 0.5) < 0.15 or features.get('bb_pct_b', 0.5) > 0.85
        # False compression: squeeze at BB extremes lacks directional conviction
        if bb_extreme:
            return "skip"
        # Also reject if VWAP deviation is extreme during compression
        if abs(features.get('vwap_deviation', 0)) > 0.01:
            return "skip"
    
    return prediction