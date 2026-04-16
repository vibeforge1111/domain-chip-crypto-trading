def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    if features.get('rsi_14', 50) > 55:
        bullish += 1
    elif features.get('rsi_14', 50) < 45:
        bearish += 1
    
    if features.get('stoch_k', 50) > 60:
        bullish += 1
    elif features.get('stoch_k', 50) < 40:
        bearish += 1
    
    if features.get('vwap_deviation', 0) > 0.002:
        bullish += 1
    elif features.get('vwap_deviation', 0) < -0.002:
        bearish += 1
    
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    if features.get('obv_slope', 0) > 0:
        bullish += 1
    elif features.get('obv_slope', 0) < 0:
        bearish += 1
    
    if prediction == "long" and bearish > 1:
        return "skip"
    if prediction == "short" and bullish > 1:
        return "skip"
    
    return prediction