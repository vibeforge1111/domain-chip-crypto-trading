def guard(features: dict, prediction: str) -> str:
    # True compression: low BB width + stable ATR
    is_compression = features.get('bb_width', 1) < 0.12
    stable_atr = features.get('atr_ratio', 1) < 1.1
    
    # False compression signals
    stoch_extreme = features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15
    vwap_far = abs(features.get('vwap_deviation', 0)) > 0.008
    
    # If in compression but has false signals, reject
    if is_compression and (stoch_extreme or vwap_far):
        return "skip"
    
    # Also reject if high ATR but high BB (expanding volatility trap)
    if features.get('atr_ratio', 1) > 1.5 and features.get('bb_width', 1) > 0.2:
        return "skip"
    
    return prediction