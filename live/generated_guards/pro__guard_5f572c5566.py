def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect compression: low ATR and narrow BB
    is_compression = atr_ratio < 0.7 and bb_width < 0.3
    
    # True compression: price near middle of BB, stoch in neutral zone
    if is_compression:
        in_middle = 0.35 <= bb_pct_b <= 0.65
        stoch_neutral = 30 <= stoch_k <= 70 and 30 <= stoch_d <= 70
        vwap_aligned = abs(vwap_deviation) < 0.005
        rsi_healthy = 40 <= rsi_2h <= 60
        
        # True compression: all conditions aligned
        if in_middle and stoch_neutral and vwap_aligned and rsi_healthy:
            return "skip"  # Skip during consolidation, likely false signal
    
    return prediction