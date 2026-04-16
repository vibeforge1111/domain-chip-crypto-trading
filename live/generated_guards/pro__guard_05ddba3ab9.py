def guard(features: dict, prediction: str) -> str:
    """Detect true compression vs false compression using atr_ratio + bb_width combo."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    
    # True compression: both metrics contracted
    is_compressed = bb_width < 0.02 and atr_ratio < 0.8
    
    # False compression signal: bands tight but volatility still elevated
    is_false_compression = bb_width < 0.02 and atr_ratio > 1.1
    
    if is_false_compression:
        return "skip"
    
    if not is_compressed:
        return "skip"
    
    # For true compression, require momentum confirmation
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    if prediction == "long":
        if stoch_k < 25 or stoch_d < 25:
            return prediction
        if stoch_k < stoch_d:
            return "skip"
    elif prediction == "short":
        if stoch_k > 75 or stoch_d > 75:
            return prediction
        if stoch_k > stoch_d:
            return "skip"
    
    return prediction