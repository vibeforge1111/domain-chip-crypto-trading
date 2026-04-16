def guard(features: dict, prediction: str) -> str:
    # True compression detection: low atr + narrow BBs
    is_compression = features['atr_ratio'] < 0.7 and features['bb_width'] < 0.015
    
    if is_compression:
        # False compression at BB extremes - likely reversal, not breakout
        bb_extreme = features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85
        rsi_extreme = features['rsi_2h'] < 30 or features['rsi_2h'] > 70
        if bb_extreme or rsi_extreme:
            return "skip"
    
    return prediction