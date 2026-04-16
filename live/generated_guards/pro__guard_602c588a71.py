def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Require 2+ indicators to agree with prediction direction
    if prediction == "long":
        if features.get('bb_pct_b', 0.5) > 0.65: confirmations += 1
        if features.get('vwap_deviation', 0) > 0.001: confirmations += 1
        if features.get('macd_histogram', 0) > 0: confirmations += 1
        if features.get('rsi_2h', 50) > 55: confirmations += 1
        if features.get('obv_slope', 0) > 0: confirmations += 1
    elif prediction == "short":
        if features.get('bb_pct_b', 0.5) < 0.35: confirmations += 1
        if features.get('vwap_deviation', 0) < -0.001: confirmations += 1
        if features.get('macd_histogram', 0) < 0: confirmations += 1
        if features.get('rsi_2h', 50) < 45: confirmations += 1
        if features.get('obv_slope', 0) < 0: confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"