def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Detect compression: tight BB + low ATR
    is_compressed = bb_width < 0.5 and atr_ratio < 0.7
    
    # False compression: compressed but at extremes with weak momentum
    at_extreme = bb_pct_b < 0.2 or bb_pct_b > 0.8
    weak_momentum = stoch_k < 30 or stoch_k > 70
    far_from_vwap = abs(vwap_deviation) > 0.02
    weak_obv = abs(obv_slope) < 0.1
    
    # Reject false compression: compressed + extreme + divergent indicators
    if is_compressed and at_extreme and weak_momentum:
        return "skip"
    
    return prediction