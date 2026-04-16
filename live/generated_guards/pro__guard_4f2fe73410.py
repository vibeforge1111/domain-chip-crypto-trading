def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter bad signals."""
    is_compression = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 0) < 0.3
    
    if is_compression:
        # False compression signals
        stoch_k = features.get('stoch_k', 50)
        stoch_d = features.get('stoch_d', 50)
        stoch_conflict = abs(stoch_k - stoch_d) > 15
        
        rsi_14 = features.get('rsi_14', 50)
        rsi_2h = features.get('rsi_2h', 50)
        tf_divergence = (rsi_14 > 60 and rsi_2h < 40) or (rsi_14 < 40 and rsi_2h > 60)
        
        vwap_far = abs(features.get('vwap_deviation', 0)) > 0.015
        
        # Skip if multiple conflicting signals during compression
        conflicts = stoch_conflict + tf_divergence + vwap_far
        if conflicts >= 2:
            return "skip"
    
    return prediction