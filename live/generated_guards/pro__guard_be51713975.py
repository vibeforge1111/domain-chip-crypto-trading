def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio, BB width, and momentum."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    macd_hist = features.get('macd_histogram', 0)
    
    # True compression: both ATR and BB are compressed
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    if prediction != "skip" and is_compressed:
        # False compression signals to reject
        weak_stoch = stoch_k < 25 or stoch_k > 75
        stoch_diverging = abs(stoch_k - stoch_d) > 12
        no_macd_confirm = (prediction == "long" and macd_hist < 0) or (prediction == "short" and macd_hist > 0)
        off_vwap = abs(vwap_dev) > 0.005
        
        if (weak_stoch and stoch_diverging) or no_macd_confirm or (weak_stoch and off_vwap):
            return "skip"
    
    return prediction