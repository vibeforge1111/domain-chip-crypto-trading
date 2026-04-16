def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using new features."""
    if features.get('bb_width', 1) < 0.5 and features.get('atr_ratio', 1) < 0.7:
        warnings = 0
        if features.get('macd_histogram', 0) < 0:
            warnings += 1
        if abs(features.get('vwap_deviation', 0)) > 0.01:
            warnings += 1
        if features.get('obv_slope', 0) < 0:
            warnings += 1
        if features.get('stoch_k', 50) - features.get('stoch_d', 50) > 15:
            warnings += 1
        if warnings >= 3:
            return 'skip'
    return prediction