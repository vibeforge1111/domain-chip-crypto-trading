def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio and bb_width."""
    atr_ratio = features.get('atr_ratio', 0.5)
    bb_width = features.get('bb_width', 0.02)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Detect compression (squeeze)
    compressed = atr_ratio < 0.65 and bb_width < 0.018
    
    if compressed:
        # False compression: bb_pct_b at extreme (price compressed to edge)
        if bb_pct_b < 0.12 or bb_pct_b > 0.88:
            return "skip"
        
        # Momentum conflict check
        if prediction == "long" and macd_histogram < -0.0002:
            return "skip"
        if prediction == "short" and macd_histogram > 0.0002:
            return "skip"
        
        # Stochastic divergence in compression
        if stoch_k > 85 or stoch_k < 15:
            return "skip"
    
    # Large VWAP deviation in compressed state signals weak/trapped
    if compressed and abs(vwap_deviation) > 0.008:
        return "skip"
    
    return prediction