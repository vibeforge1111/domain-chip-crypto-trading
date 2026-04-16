def guard(features: dict, prediction: str) -> str:
    # False compression: bb_width tight but atr_ratio elevated = fake breakout setup
    is_false_compression = features['bb_width'] < 0.12 and features['atr_ratio'] > 1.1
    
    if is_false_compression:
        return "skip"
    
    # True compression check: both bb_width and atr_ratio low
    is_true_squeeze = features['bb_width'] < 0.1 and features['atr_ratio'] < 0.85
    
    # During true squeeze, avoid entries at band extremes
    if is_true_squeeze:
        if features['bb_pct_b'] < 0.08 or features['bb_pct_b'] > 0.92:
            return "skip"
    
    return prediction