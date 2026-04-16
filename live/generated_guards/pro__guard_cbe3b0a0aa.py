def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, BB, and momentum divergence."""
    atr = features.get("atr_ratio", 1.0)
    bb_w = features.get("bb_width", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    
    # Compression detection: both ATR and BB narrow
    is_compressed = atr < 0.7 and bb_w < 0.25
    
    if is_compressed:
        # Momentum divergence: short-term overbought/oversold vs 2h context
        short_extreme = stoch_k > 80 or stoch_k < 20
        rsi_divergent = (rsi_2h > 60 and stoch_k < 30) or (rsi_2h < 40 and stoch_k > 70)
        
        # Weak volume confirmation during compression
        weak_obv = obv_slope < 0 and macd_hist < 0 if prediction == "long" else obv_slope > 0 and macd_hist > 0
        
        if short_extreme and rsi_divergent and weak_obv:
            return "skip"
    
    return prediction