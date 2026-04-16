def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and momentum features."""
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.02)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect compression: low atr + tight bands
    is_compressed = atr_ratio < 0.7 and bb_width < 0.025
    
    if is_compressed:
        # Reject if stochastics diverging (false compression signal)
        if abs(stoch_k - stoch_d) > 20:
            return "skip"
        
        # Reject if at band extremes (likely reversal incoming)
        if bb_pct_b > 0.92 or bb_pct_b < 0.08:
            return "skip"
        
        # For longs: price should be above VWAP
        if prediction == "long" and vwap_dev < -0.005:
            return "skip"
        
        # For shorts: price should be below VWAP
        if prediction == "short" and vwap_dev > 0.005:
            return "skip"
        
        # Reject if momentum contradicts direction
        if prediction == "long" and macd_hist < 0 and obv_slope < 0:
            return "skip"
        if prediction == "short" and macd_hist > 0 and obv_slope > 0:
            return "skip"
        
        # Reject if 2h RSI too extended (mean reversion risk)
        if rsi_2h > 78 or rsi_2h < 22:
            return "skip"
    
    return prediction