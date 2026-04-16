def guard(features: dict, prediction: str) -> str:
    """Filter signals during false compression patterns."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # False compression: tight BB but elevated ATR indicates noisy chop
    false_compression = bb_width < 0.15 and atr_ratio > 1.3
    
    # Price too far from VWAP suggests weak conviction
    vwap_extreme = abs(features.get('vwap_deviation', 0)) > 0.02
    
    # RSI divergence between timeframes weakens the signal
    rsi_div = abs(features.get('rsi_14', 50) - features.get('rsi_2h', 50))
    rsi_divergent = rsi_div > 25
    
    if false_compression or vwap_extreme or rsi_divergent:
        return "skip"
    
    return prediction