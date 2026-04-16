def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) < 40:
        bullish_count += 1
    elif features.get('rsi_14', 50) > 60:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 30:
        bullish_count += 1
    elif features.get('stoch_k', 50) > 70:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish_count += 1
    elif features.get('vwap_deviation', 0) < 0:
        bearish_count += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # RSI 2h confirmation
    if features.get('rsi_2h', 50) < 45:
        bullish_count += 1
    elif features.get('rsi_2h', 50) > 55:
        bearish_count += 1
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction