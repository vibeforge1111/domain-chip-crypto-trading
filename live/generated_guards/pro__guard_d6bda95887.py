def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using BB metrics and momentum."""
    if prediction == "skip":
        return prediction
    
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Detect compression: both bb_width and atr_ratio are low
    is_compression = bb_width < 0.7 and atr_ratio < 0.8
    
    if is_compression:
        # False compression: price at extreme BB position
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
        
        # False compression: RSI divergence between timeframes
        if (prediction == "long" and rsi_2h > 65 and rsi_14 < 40) or \
           (prediction == "short" and rsi_2h < 35 and rsi_14 > 60):
            return "skip"
        
        # False compression: stochastic at extreme with no momentum
        if stoch_k < 15 and vwap_deviation < -0.005:
            return "skip"
    
    return prediction