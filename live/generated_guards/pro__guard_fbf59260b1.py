def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect true compression: low BB width AND low ATR ratio
    is_compression = bb_width < 0.015 and atr_ratio < 0.8
    
    if is_compression:
        # False compression: price at band extremes with extreme stoch
        at_extreme = (bb_pct_b > 0.85 or bb_pct_b < 0.15) and (stoch_k > 80 or stoch_k < 20)
        # Also check wider context confirms exhaustion
        context_exhausted = (rsi_2h > 70 or rsi_2h < 30)
        
        if at_extreme and context_exhausted:
            return "skip"
    
    return prediction