def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    bullish = 0
    bearish = 0
    
    if features['rsi_14'] > 40 and features['rsi_14'] < 60:
        bullish += 1
    elif features['rsi_14'] > 60:
        bearish += 1
    
    if features['stoch_k'] > 25:
        bullish += 1
    elif features['stoch_k'] < 75:
        bearish += 1
    
    if features['macd_histogram'] > 0:
        bullish += 1
    else:
        bearish += 1
    
    if features['obv_slope'] > 0:
        bullish += 1
    else:
        bearish += 1
    
    if prediction == "long" and bullish >= 2:
        return prediction
    if prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"