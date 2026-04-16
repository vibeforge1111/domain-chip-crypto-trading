def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    if features.get("rsi_14", 50) < 60:
        bullish_signals += 1
    if features.get("rsi_14", 50) > 40:
        bearish_signals += 1
    
    if features.get("stoch_k", 50) < 75:
        bullish_signals += 1
    if features.get("stoch_k", 50) > 25:
        bearish_signals += 1
    
    if features.get("vwap_deviation", 0) > 0:
        bullish_signals += 1
    if features.get("vwap_deviation", 0) < 0:
        bearish_signals += 1
    
    if features.get("obv_slope", 0) > 0:
        bullish_signals += 1
    if features.get("obv_slope", 0) < 0:
        bearish_signals += 1
    
    if features.get("macd_histogram", 0) > 0:
        bullish_signals += 1
    if features.get("macd_histogram", 0) < 0:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    if prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"