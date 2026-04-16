def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using ATR, BB, VWAP, and momentum."""
    # Require compression (low ATR ratio)
    if features.get('atr_ratio', 1) > 0.85:
        return "skip"
    
    # Require BB compression
    if features.get('bb_width', 1) > 0.4:
        return "skip"
    
    # False compression: price too far from VWAP (mean reversion likely)
    if abs(features.get('vwap_deviation', 0)) > 0.015:
        return "skip"
    
    # False compression: stochastic extremes (reversal risk)
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    
    # False compression: OBV/momentum divergence
    if features.get('obv_slope', 0) * features.get('macd_histogram', 0) < 0:
        return "skip"
    
    return prediction