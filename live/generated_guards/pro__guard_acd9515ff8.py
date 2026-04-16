def guard(features: dict, prediction: str) -> str:
    """Detect false compression using bb_width, atr_ratio, and warning signals."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)

    is_compression = bb_width < 0.18 and atr_ratio < 0.8
    is_mid_range = 0.3 < bb_pct_b < 0.7
    is_vwap_far = abs(vwap_deviation) > 0.008
    is_weak_momentum = abs(macd_histogram) < 0.0003 and abs(obv_slope) < 0.5

    if is_compression and is_mid_range and is_vwap_far and is_weak_momentum:
        return "skip"

    return prediction