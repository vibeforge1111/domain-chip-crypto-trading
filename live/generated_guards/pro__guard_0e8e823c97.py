def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Count how many indicators agree with the prediction
    agree_count = 0
    
    if prediction == "long":
        if features['stoch_k'] < 25:
            agree_count += 1
        if features['vwap_deviation'] > 0:
            agree_count += 1
        if features['macd_histogram'] > 0:
            agree_count += 1
        if features['bb_pct_b'] < 0.2:
            agree_count += 1
        if features['obv_slope'] > 0:
            agree_count += 1
    else:
        if features['stoch_k'] > 75:
            agree_count += 1
        if features['vwap_deviation'] < 0:
            agree_count += 1
        if features['macd_histogram'] < 0:
            agree_count += 1
        if features['bb_pct_b'] > 0.8:
            agree_count += 1
        if features['obv_slope'] < 0:
            agree_count += 1
    
    # Require at least 2 indicators to agree
    if agree_count < 2:
        return "skip"
    
    return prediction