def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Long confirmations from new indicators
    if features.get('macd_histogram', 0) > 0:
        confirmations += 1
    if features.get('obv_slope', 0) > 0:
        confirmations += 1
    if features.get('vwap_deviation', 0) > 0:
        confirmations += 1
    if features.get('bb_pct_b', 0.5) > 0.6:
        confirmations += 1
    if features.get('stoch_k', 50) > 60:
        confirmations += 1
    
    # Short confirmations from new indicators
    if features.get('macd_histogram', 0) < 0:
        confirmations += 1
    if features.get('obv_slope', 0) < 0:
        confirmations += 1
    if features.get('vwap_deviation', 0) < 0:
        confirmations += 1
    if features.get('bb_pct_b', 0.5) < 0.4:
        confirmations += 1
    if features.get('stoch_k', 50) < 40:
        confirmations += 1
    
    # Require 2+ confirmations and no extreme RSI
    rsi = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == "long" and (rsi > 70 or rsi_2h > 75):
        return "skip"
    if prediction == "short" and (rsi < 30 or rsi_2h < 25):
        return "skip"
    
    if confirmations < 2:
        return "skip"
    
    return prediction