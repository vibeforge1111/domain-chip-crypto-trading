def guard(features: dict, prediction: str) -> str:
    """Filter trades during compressed market conditions with momentum confirmation."""
    # Detect compression: low ATR + narrow BB
    is_compression = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 1) < 0.3
    
    if is_compression:
        # During compression, skip if stochastics diverge (one below 30, other above 70)
        stoch_k = features.get('stoch_k', 50)
        stoch_d = features.get('stoch_d', 50)
        if (stoch_k < 30 and stoch_d > 70) or (stoch_k > 70 and stoch_d < 30):
            return "skip"
        
        # During compression, require OBV momentum alignment with prediction
        obv_slope = features.get('obv_slope', 0)
        if prediction == "long" and obv_slope < 0:
            return "skip"
        if prediction == "short" and obv_slope > 0:
            return "skip"
        
        # Skip if too close to BB edge after breakout (potential exhaustion)
        if features.get('bb_pct_b', 0.5) > 0.95 or features.get('bb_pct_b', 0.5) < 0.05:
            return "skip"
    
    return prediction