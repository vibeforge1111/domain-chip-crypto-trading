def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using multi-indicator validation."""
    if prediction == "skip":
        return prediction
    
    # Detect true compression: low BB width AND low ATR ratio
    is_compression = features.get('bb_width', 1) < 0.12 and features.get('atr_ratio', 1) < 0.65
    
    if is_compression:
        # Position within bands (middle = true compression)
        bb_pct = features.get('bb_pct_b', 0.5)
        in_middle = 0.35 < bb_pct < 0.65
        
        # Direction validation using 2h RSI and stochastics
        stoch = features.get('stoch_k', 50)
        rsi_2h = features.get('rsi_2h', 50)
        
        if prediction == "long":
            valid_direction = stoch > 40 and rsi_2h > 45
            vwap_ok = features.get('vwap_deviation', 0) >= -0.002
        else:
            valid_direction = stoch < 60 and rsi_2h < 55
            vwap_ok = features.get('vwap_deviation', 0) <= 0.002
        
        # Require momentum alignment via MACD
        macd_ok = features.get('macd_histogram', 0) > 0 if prediction == "long" else features.get('macd_histogram', 0) < 0
        
        # Reject if compression but not in middle, or momentum disagrees
        if not in_middle or not valid_direction or not vwap_ok or not macd_ok:
            return "skip"
    
    return prediction