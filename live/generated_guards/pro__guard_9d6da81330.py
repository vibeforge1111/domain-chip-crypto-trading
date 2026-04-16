def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, Bollinger width, and momentum."""
    atr = features.get("atr_ratio", 1.0)
    bb_w = features.get("bb_width", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    obv = features.get("obv_slope", 0)
    
    # True compression: both ATR and BB width are low
    in_compression = atr < 0.7 and bb_w < 0.3
    
    if in_compression:
        # False compression signals
        stoch_stretch = stoch_k > 80 or stoch_k < 20
        rsi_div = (rsi_2h > 70 and features.get("rsi_14", 50) < 55) or (rsi_2h < 30 and features.get("rsi_14", 50) > 45)
        no_volume = obv < 0
        
        if stoch_stretch and rsi_div:
            return "skip"
        if no_volume and (stoch_stretch or rsi_div):
            return "skip"
    
    return prediction