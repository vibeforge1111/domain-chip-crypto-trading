def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    macd_hist = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price far above VWAP but momentum weak = bearish disagreement
    if vwap_dev > 0.005 and stoch_k < 30 and macd_hist < 0:
        return "skip"
    
    # Price far below VWAP but momentum strong = bullish disagreement
    if vwap_dev < -0.005 and stoch_k > 70 and macd_hist > 0:
        return "skip"
    
    # Additional filter: 2h RSI contradicts VWAP position
    if vwap_dev > 0.01 and rsi_2h < 40:
        return "skip"
    if vwap_dev < -0.01 and rsi_2h > 60:
        return "skip"
    
    return prediction