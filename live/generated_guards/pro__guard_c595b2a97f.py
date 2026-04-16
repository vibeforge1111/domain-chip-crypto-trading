def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, BB width, VWAP and momentum."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: narrow bands + low ATR
    is_compressed = bb_width < 0.12 and atr_ratio < 0.65
    
    # Price near VWAP confirms true compression
    near_vwap = abs(vwap_dev) < 0.003
    
    # Momentum stretched, ready for reversal
    momentum_extreme = stoch_k < 25 or stoch_k > 75
    
    # 2h context neutral (not diverging against trade)
    neutral_2h = 35 < rsi_2h < 65
    
    if is_compressed and near_vwap and momentum_extreme and neutral_2h:
        return prediction
    return "skip"