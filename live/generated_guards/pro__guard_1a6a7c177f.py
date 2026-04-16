def guard(features: dict, prediction: str) -> str:
    # True compression: both ATR and BB width compressed
    is_compressed = features['atr_ratio'] < 0.8 and features['bb_width'] < 0.15
    
    # False compression trap: low ATR but wide BB (contradiction = potential trap)
    is_false_compression = features['atr_ratio'] < 0.8 and features['bb_width'] > 0.25
    
    if is_false_compression:
        return "skip"
    
    if is_compressed and prediction != "skip":
        # Near band extremes during compression often precedes breakouts - skip
        if features['bb_pct_b'] > 0.92 or features['bb_pct_b'] < 0.08:
            return "skip"
        
        # True compression should have low VWAP deviation
        if abs(features['vwap_deviation']) > 0.012:
            return "skip"
        
        # Align with 2h RSI trend
        if prediction == "long" and features['rsi_2h'] < 40:
            return "skip"
        if prediction == "short" and features['rsi_2h'] > 60:
            return "skip"
    
    return prediction