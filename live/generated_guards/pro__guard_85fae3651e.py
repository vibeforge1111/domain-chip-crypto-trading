def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    if prediction == "long":
        if features.get('macd_histogram', 0) > 0:
            agree_count += 1
        if features.get('vwap_deviation', 0) > 0:
            agree_count += 1
        if features.get('obv_slope', 0) > 0:
            agree_count += 1
        if features.get('stoch_k', 50) < 80:
            agree_count += 1
        if features.get('rsi_2h', 50) < 70:
            agree_count += 1
    elif prediction == "short":
        if features.get('macd_histogram', 0) < 0:
            agree_count += 1
        if features.get('vwap_deviation', 0) < 0:
            agree_count += 1
        if features.get('obv_slope', 0) < 0:
            agree_count += 1
        if features.get('stoch_k', 50) > 20:
            agree_count += 1
        if features.get('rsi_2h', 50) > 30:
            agree_count += 1
    
    return "skip" if agree_count < 2 else prediction