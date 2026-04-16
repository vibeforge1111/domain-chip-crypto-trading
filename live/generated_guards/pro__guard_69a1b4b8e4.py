def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    long_count = 0
    short_count = 0
    
    if features.get('rsi_14', 50) < 70:
        long_count += 1
    if features.get('rsi_14', 50) > 30:
        short_count += 1
    
    if features.get('macd_histogram', 0) > 0:
        long_count += 1
    if features.get('macd_histogram', 0) < 0:
        short_count += 1
    
    if features.get('vwap_deviation', 0) > 0:
        long_count += 1
    if features.get('vwap_deviation', 0) < 0:
        short_count += 1
    
    if features.get('obv_slope', 0) > 0:
        long_count += 1
    if features.get('obv_slope', 0) < 0:
        short_count += 1
    
    if features.get('stoch_k', 50) < 80:
        long_count += 1
    if features.get('stoch_k', 50) > 20:
        short_count += 1
    
    if prediction == "long" and long_count < 2:
        return "skip"
    if prediction == "short" and short_count < 2:
        return "skip"
    
    return prediction