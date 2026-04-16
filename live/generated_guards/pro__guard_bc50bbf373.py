def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    
    # True compression: both ATR and BB compressed
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    if is_compressed:
        # False compression often has price away from VWAP
        vwap_deviation = features.get("vwap_deviation", 0)
        if abs(vwap_deviation) > 0.008:
            return "skip"
        
        # Check RSI divergence between timeframes
        rsi_14 = features.get("rsi_14", 50)
        rsi_2h = features.get("rsi_2h", 50)
        if abs(rsi_14 - rsi_2h) > 25:
            return "skip"
        
        # Momentum should be building in true compression
        macd_histogram = features.get("macd_histogram", 0)
        if abs(macd_histogram) < 0.0002:
            return "skip"
    
    return prediction