def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Long confirmations
    if prediction == "long":
        if features.get('rsi_14', 50) < 70 and features.get('rsi_14', 50) > 40:
            confirmations += 1
        if features.get('stoch_k', 50) < 80:
            confirmations += 1
        if features.get('vwap_deviation', 0) > -0.02:
            confirmations += 1
        if features.get('obv_slope', 0) > 0:
            confirmations += 1
        if features.get('macd_histogram', 0) > 0:
            confirmations += 1
    
    # Short confirmations
    elif prediction == "short":
        if features.get('rsi_14', 50) > 30 and features.get('rsi_14', 50) < 60:
            confirmations += 1
        if features.get('stoch_k', 50) > 20:
            confirmations += 1
        if features.get('vwap_deviation', 0) < 0.02:
            confirmations += 1
        if features.get('obv_slope', 0) < 0:
            confirmations += 1
        if features.get('macd_histogram', 0) < 0:
            confirmations += 1
    
    return "skip" if confirmations < 2 else prediction