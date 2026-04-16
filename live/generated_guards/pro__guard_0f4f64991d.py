def guard(features: dict, prediction: str) -> str:
    """Filter trades when compression exists but momentum diverges."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    obv_slope = features.get('obv_slope', 0.0)
    vwap_dev = features.get('vwap_deviation', 0.0)
    
    # True compression: low ATR ratio AND narrow BB width
    is_compression = atr_ratio < 0.7 and bb_width < 0.4
    
    if is_compression:
        # Skip long if RSI in wider timeframe is elevated (bearish divergence)
        if prediction == "long" and (rsi_2h > 65 or obv_slope < -0.01 or vwap_dev < -0.015):
            return "skip"
        # Skip short if RSI in wider timeframe is suppressed (bullish divergence)
        if prediction == "short" and (rsi_2h < 35 or obv_slope > 0.01 or vwap_dev > 0.015):
            return "skip"
    
    return prediction