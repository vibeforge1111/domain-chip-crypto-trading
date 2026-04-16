def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    if prediction == "long":
        if features.get('rsi_14', 50) < 70: confirmations += 1
        if features.get('rsi_2h', 50) < 70: confirmations += 1
        if features.get('stoch_k', 50) < 80: confirmations += 1
        if features.get('vwap_deviation', 0) > 0: confirmations += 1
        if features.get('macd_histogram', 0) > 0: confirmations += 1
        if features.get('obv_slope', 0) > 0: confirmations += 1
        if features.get('bb_pct_b', 0.5) > 0.5: confirmations += 1
    elif prediction == "short":
        if features.get('rsi_14', 50) > 30: confirmations += 1
        if features.get('rsi_2h', 50) > 30: confirmations += 1
        if features.get('stoch_k', 50) > 20: confirmations += 1
        if features.get('vwap_deviation', 0) < 0: confirmations += 1
        if features.get('macd_histogram', 0) < 0: confirmations += 1
        if features.get('obv_slope', 0) < 0: confirmations += 1
        if features.get('bb_pct_b', 0.5) < 0.5: confirmations += 1
    
    return "skip" if confirmations < 2 else prediction