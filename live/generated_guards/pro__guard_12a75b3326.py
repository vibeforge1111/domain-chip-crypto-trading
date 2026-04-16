def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirm = 0
    
    # For long signals
    if prediction == "long":
        if features['vwap_deviation'] > 0:
            confirm += 1
        if features['macd_histogram'] > 0:
            confirm += 1
        if features['obv_slope'] > 0:
            confirm += 1
        if features['rsi_2h'] > 50:
            confirm += 1
        if features['bb_pct_b'] > 0.6:
            confirm += 1
    
    # For short signals
    elif prediction == "short":
        if features['vwap_deviation'] < 0:
            confirm += 1
        if features['macd_histogram'] < 0:
            confirm += 1
        if features['obv_slope'] < 0:
            confirm += 1
        if features['rsi_2h'] < 50:
            confirm += 1
        if features['bb_pct_b'] < 0.4:
            confirm += 1
    
    return "skip" if confirm < 2 else prediction