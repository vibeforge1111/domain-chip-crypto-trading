def guard(features: dict, prediction: str) -> str:
    # True compression: tight BB + low ATR, good for breakout
    # False compression: tight BB + price at extremes + divergent momentum
    if features['bb_width'] < 0.12 and features['atr_ratio'] < 0.75:
        # Check for false compression: price at BB extremes
        if features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85:
            return "skip"
        # Check for divergent momentum
        if features['obv_slope'] < 0 and features['macd_histogram'] > 0:
            return "skip"
        if features['obv_slope'] > 0 and features['macd_histogram'] < 0:
            return "skip"
        # Check for VWAP deviation during compression
        if abs(features['vwap_deviation']) > 0.008:
            return "skip"
    return prediction