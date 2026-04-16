def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    long_signals = 0
    if features.get('stoch_k', 50) < 75:
        long_signals += 1
    if features.get('stoch_d', 50) < 75:
        long_signals += 1
    if features.get('vwap_deviation', 0) > 0.001:
        long_signals += 1
    if features.get('macd_histogram', 0) > 0:
        long_signals += 1
    if features.get('obv_slope', 0) > 0:
        long_signals += 1
    if features.get('rsi_2h', 50) < 60:
        long_signals += 1
    
    short_signals = 0
    if features.get('stoch_k', 50) > 25:
        short_signals += 1
    if features.get('stoch_d', 50) > 25:
        short_signals += 1
    if features.get('vwap_deviation', 0) < -0.001:
        short_signals += 1
    if features.get('macd_histogram', 0) < 0:
        short_signals += 1
    if features.get('obv_slope', 0) < 0:
        short_signals += 1
    if features.get('rsi_2h', 50) > 40:
        short_signals += 1
    
    if prediction == "long" and long_signals < 2:
        return "skip"
    if prediction == "short" and short_signals < 2:
        return "skip"
    
    return prediction