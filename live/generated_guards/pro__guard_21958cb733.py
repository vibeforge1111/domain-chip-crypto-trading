def guard(features: dict, prediction: str) -> str:
    """Filter signals during compression phases using ATR, BB, and momentum."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_histogram = features.get('macd_histogram', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: both ATR and BB are low
    is_compression = atr_ratio < 0.75 and bb_width < 0.35
    
    if is_compression:
        # Skip if price at extreme BB position during compression
        if bb_pct_b > 0.88 or bb_pct_b < 0.12:
            return "skip"
        # Skip if RSI overbought/oversold in both timeframes
        if rsi_14 > 72 or rsi_14 < 28 or rsi_2h > 72 or rsi_2h < 28:
            return "skip"
        # Skip if momentum diverges from prediction
        if prediction == "long" and macd_histogram < -0.0001:
            return "skip"
        if prediction == "short" and macd_histogram > 0.0001:
            return "skip"
        # Skip if price far from VWAP during compression
        if abs(vwap_deviation) > 0.015:
            return "skip"
    
    return prediction