def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and new features."""
    is_compressed = features['atr_ratio'] < 0.7 and features['bb_width'] < 0.3
    
    if is_compressed and prediction != "skip":
        # False compression signals: BB at extremes, far from VWAP, overbought/oversold
        bb_extreme = features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85
        vwap_far = abs(features['vwap_deviation']) > 0.01
        stoch_extreme = features['stoch_k'] > 80 or features['stoch_k'] < 20
        
        # Skip if multiple false compression indicators present
        if sum([bb_extreme, vwap_far, stoch_extreme]) >= 2:
            return "skip"
    
    return prediction