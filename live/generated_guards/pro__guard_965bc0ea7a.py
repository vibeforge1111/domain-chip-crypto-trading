def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    long_confirm = 0
    short_confirm = 0
    
    if features.get('stoch_k', 50) < 70:
        long_confirm += 1
    if features.get('stoch_k', 50) > 30:
        short_confirm += 1
    
    if features.get('vwap_deviation', 0) > 0:
        long_confirm += 1
    if features.get('vwap_deviation', 0) < 0:
        short_confirm += 1
    
    if features.get('macd_histogram', 0) > 0:
        long_confirm += 1
    if features.get('macd_histogram', 0) < 0:
        short_confirm += 1
    
    if features.get('obv_slope', 0) > 0:
        long_confirm += 1
    if features.get('obv_slope', 0) < 0:
        short_confirm += 1
    
    if features.get('bb_pct_b', 0.5) < 0.6:
        long_confirm += 1
    if features.get('bb_pct_b', 0.5) > 0.4:
        short_confirm += 1
    
    if features.get('rsi_2h', 50) < 65:
        long_confirm += 1
    if features.get('rsi_2h', 50) > 35:
        short_confirm += 1
    
    if prediction == "long" and long_confirm < 3:
        return "skip"
    if prediction == "short" and short_confirm < 3:
        return "skip"
    
    return prediction