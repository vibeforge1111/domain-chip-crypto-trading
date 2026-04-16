def guard(features: dict, prediction: str) -> str:
    # Detect true compression: both atr and bb contracted
    in_compression = features['atr_ratio'] < 0.75 and features['bb_width'] < 0.5
    
    if in_compression:
        # False compression signals: mid-range bb + neutral stoch + weak obv
        mid_range = 0.35 <= features['bb_pct_b'] <= 0.65
        stoch_flat = abs(features['stoch_k'] - features['stoch_d']) < 12
        obv_weak = features['obv_slope'] < 0.05
        
        if mid_range and stoch_flat and obv_weak:
            return "skip"
    
    return prediction