def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: narrow BB + potential ATR expansion
    if bb_width >= 0.5 or atr_ratio < 0.6:
        return "skip"
    
    # Momentum must confirm direction (not overbought/oversold)
    if prediction == "long":
        if not (macd_histogram > 0 and 25 < stoch_k < 75):
            return "skip"
        if obv_slope < 0 or vwap_deviation < -0.003:
            return "skip"
    elif prediction == "short":
        if not (macd_histogram < 0 and 25 < stoch_k < 75):
            return "skip"
        if obv_slope > 0 or vwap_deviation > 0.003:
            return "skip"
    
    return prediction