def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Compression: both volatility measures are low
    is_compression = bb_width < 0.15 and atr_ratio < 0.8
    
    if not is_compression:
        return prediction
    
    # False compression: price at BB edge with weak momentum/volume
    near_edge = bb_pct_b < 0.15 or bb_pct_b > 0.85
    weak_momentum = macd_histogram < 0
    weak_volume = obv_slope <= 0
    
    if near_edge and (weak_momentum or weak_volume):
        return "skip"
    
    # True compression: price centered with confirming signals
    centered = abs(bb_pct_b - 0.5) < 0.2
    near_vwap = abs(vwap_deviation) < 0.005
    good_momentum = macd_histogram > 0
    
    # Only accept compression setups with multiple confirming signals
    confirm_count = (centered and near_vwap) + good_momentum + (obv_slope > 0)
    if is_compression and confirm_count < 2:
        return "skip"
    
    return prediction