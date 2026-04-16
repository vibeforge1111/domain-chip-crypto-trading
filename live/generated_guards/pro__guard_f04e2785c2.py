def guard(features: dict, prediction: str) -> str:
    # Detect true compression: both ATR and BB tight
    is_compressed = features.get('atr_ratio', 1.0) < 0.7 and features.get('bb_width', 0.5) < 0.5
    
    # For compression setups, require structural alignment
    if is_compressed:
        bb_pos = features.get('bb_pct_b', 0.5)
        vwap_dev = features.get('vwap_deviation', 0)
        
        # Long only if price near bottom of BB and above/slightly below VWAP
        if prediction == 'long' and (bb_pos < 0.2 or vwap_dev < -0.015):
            return "skip"
        # Short only if price near top of BB and above VWAP
        if prediction == 'short' and (bb_pos > 0.8 or vwap_dev > 0.015):
            return "skip"
    
    return prediction