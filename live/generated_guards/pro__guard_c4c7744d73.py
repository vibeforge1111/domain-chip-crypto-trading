def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    
    Focus: bb_pct_b extremes (<0.05 or >0.95) as high-confidence entry zones
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Long signals only at lower band extreme with confirmation
    if prediction == "long":
        if bb_pct_b < 0.05 and rsi_14 < 70 and stoch_k < 80:
            if volume_ratio >= 0.8:
                return prediction
    
    # Short signals only at upper band extreme with confirmation
    if prediction == "short":
        if bb_pct_b > 0.95 and rsi_14 > 30 and stoch_k > 20:
            if volume_ratio >= 0.8:
                return prediction
    
    return "skip"