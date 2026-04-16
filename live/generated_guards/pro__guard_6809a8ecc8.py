def guard(features: dict, prediction: str) -> str:
    # Detect true compression: both low BB width and low ATR
    is_compressed = features['bb_width'] < 0.12 and features['atr_ratio'] < 0.75
    
    if is_compressed and prediction != "skip":
        # False compression often shows extreme BB position + divergent stoch
        bb_extreme = features['bb_pct_b'] > 0.8 or features['bb_pct_b'] < 0.2
        stoch_divergent = abs(features['stoch_k'] - features['stoch_d']) > 15
        stoch_extreme = features['stoch_k'] > 75 or features['stoch_k'] < 25
        
        # Skip if compression has extreme readings suggesting false signal
        if bb_extreme and stoch_extreme and stoch_divergent:
            return "skip"
    
    return prediction