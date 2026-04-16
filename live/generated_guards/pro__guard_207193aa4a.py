def guard(features: dict, prediction: str) -> str:
    """Detect false compression using volatility and momentum divergence."""
    # True compression: low ATR ratio AND narrow BB width
    is_compression = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 1) < 0.35
    
    if is_compression and prediction != "skip":
        # False compression signals
        stoch_exhausted = features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15
        vwap_drift = abs(features.get('vwap_deviation', 0)) > 0.015
        volume_diverging = features.get('obv_slope', 0) < 0
        
        if stoch_exhausted or vwap_drift or volume_diverging:
            return "skip"
    
    return prediction