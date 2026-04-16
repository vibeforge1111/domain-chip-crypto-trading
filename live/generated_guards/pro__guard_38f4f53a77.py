def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Long confirmation signals
    if prediction == "long":
        if features['rsi_14'] > 40:
            confirmations += 1
        if features['stoch_k'] > 30:
            confirmations += 1
        if features['vwap_deviation'] > 0:
            confirmations += 1
        if features['macd_histogram'] > 0:
            confirmations += 1
        if features['obv_slope'] > 0:
            confirmations += 1
    else:  # short
        if features['rsi_14'] < 60:
            confirmations += 1
        if features['stoch_k'] < 70:
            confirmations += 1
        if features['vwap_deviation'] < 0:
            confirmations += 1
        if features['macd_histogram'] < 0:
            confirmations += 1
        if features['obv_slope'] < 0:
            confirmations += 1
    
    return "skip" if confirmations < 2 else prediction